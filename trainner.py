# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import math
import time
import sys
import pandas as pd
import numpy as np
import tensorflow as tf
from IPython import display
from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
from tensorflow import keras
from tensorflow.python.data import Dataset
from sklearn import metrics
from sklearn.metrics import roc_curve

def construct_feature_columns(input_features):
  return set([tf.feature_column.numeric_column(my_features)
              for my_features in input_features])
'''
def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
  features = {key:np.array(value) for key,value in dict(features).items()}

  ds = Dataset.from_tensor_slices((features, targets))
  ds = ds.batch(batch_size).repeat(num_epochs)

  if shuffle:
      ds = ds.shuffle(buffer_size=200)

  features, labels = ds.make_one_shot_iterator().get_next()
  return features, labels
'''

def make_input_fn(X, y, n_epochs=None, shuffle=True):
  def input_fn():
    dataset = tf.data.Dataset.from_tensor_slices((dict(X), y))
    if shuffle:
      dataset = dataset.shuffle(NUM_EXAMPLES)
    # For training, cycle thru dataset as many times as need (n_epochs=None).    
    dataset = dataset.repeat(n_epochs)  
    # In memory training doesn't use batching.
    dataset = dataset.batch(NUM_EXAMPLES)
    return dataset
  return input_fn



def train_boosted_trees_model(
    learning_rate,
    l1_regularization_strength,
    l2_regularization_strength,
    n_batches_per_layer,
    n_trees,
    max_depth,
    steps,
    batch_size,
    tree_complexity,
    min_node_weight,
    training_examples,
    training_targets,
    validation_examples,
    validation_targets):

  # Model save path
  dir_path = os.path.dirname(os.path.realpath(__file__))
  models_path=os.path.join(dir_path,'models/'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'/')
  # Create a DNNRegressor object.
  #my_optimizer = tf.train.FtrlOptimizer(
  #                 learning_rate=learning_rate, 
  #                 l1_regularization_strength=l1_regularization_strength, 
  #                 l2_regularization_strength=l2_regularization_strength)
  #my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  classifier = tf.estimator.BoostedTreesClassifier(
      feature_columns=construct_feature_columns(training_examples),
      n_batches_per_layer=n_batches_per_layer,
      n_classes=3,
      n_trees=n_trees,
      max_depth=max_depth,
      learning_rate=learning_rate,
      l1_regularization=l1_regularization_strength,
      l2_regularization=l2_regularization_strength,
      tree_complexity=tree_complexity,
      min_node_weight=min_node_weight,
      config=tf.contrib.learn.RunConfig(keep_checkpoint_max=1),
      model_dir=models_path
  )
  '''
  # Create input functions.
  training_input_fn = lambda: my_input_fn(training_examples, 
                                          training_targets, 
                                          batch_size=batch_size)
  predict_training_input_fn = lambda: my_input_fn(training_examples, 
                                                  training_targets, 
                                                  num_epochs=1, 
                                                  shuffle=False)
  predict_validation_input_fn = lambda: my_input_fn(validation_examples, 
                                                    validation_targets, 
                                                    num_epochs=1, 
                                                    shuffle=False)
                                                    '''
  # Training and evaluation input functions.
  train_input_fn = make_input_fn(training_examples, training_targets)
  eval_input_fn = make_input_fn(validation_examples, validation_targets, shuffle=False, n_epochs=1)
  # Train the model
  print("Training model...")
  # Train the model, starting from the prior state.
  classifier.train(
      input_fn=train_input_fn,
      max_steps=steps
  )

  results = classifier.evaluate(eval_input_fn)
  pd.Series(results).to_csv(os.path.join(models_path, 'result.csv'))

  print("Model training finished.")

  # Remove event files to save disk space.
  #_ = map(os.remove, glob.glob(os.path.join(classifier.model_dir, 'events.out.tfevents*')))

  pred_dicts = list(classifier.predict(eval_input_fn))
  probs = pd.Series([pred['probabilities'][1] for pred in pred_dicts])
  probs.plot(kind='hist', bins=20, title='predicted probabilities')
  plt.savefig(os.path.join(models_path, "predicted_probabilities.png"))
  plt.draw()
  plt.close()

  # Output a graph of loss metrics over periods.
  #fpr, tpr, _ = roc_curve(validation_targets, probs)
  #plt.plot(fpr, tpr)
  #plt.title('ROC curve')
  #plt.xlabel('false positive rate')
  #plt.ylabel('true positive rate')
  #plt.xlim(0,)
  #plt.ylim(0,)
  #plt.savefig(os.path.join(models_path, "roc.png"))
  
  feature_spec = tf.feature_column.make_parse_example_spec(construct_feature_columns(training_examples))
  print(feature_spec)
  serving_input_receiver_fn = \
      tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)
  export_model = classifier.export_savedmodel(os.path.join(models_path, 'export/'), serving_input_receiver_fn)

  return classifier

if __name__ == '__main__':
  tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
  gene_df = pd.read_csv('ready2train/'+sys.argv[1]+'.csv', header=0)
  gene_df = gene_df.reindex(np.random.permutation(gene_df.index))
  training_examples = gene_df.drop('Label', axis=1).head(170)
  training_targets = gene_df['Label'].head(170)
  validation_examples = gene_df.drop('Label', axis=1).tail(53)
  validation_targets = gene_df['Label'].tail(53)
  NUM_EXAMPLES = len(training_targets)
  classifier = train_boosted_trees_model(
      learning_rate=0.01,
      l1_regularization_strength=0.1,
      l2_regularization_strength=0.1,
      n_batches_per_layer=10,
      n_trees=100,
      max_depth=6,
      steps=1000,
      batch_size=100,
      tree_complexity=0.0,
      min_node_weight=0.0,
      training_examples=training_examples,
      training_targets=training_targets,
      validation_examples=validation_examples,
      validation_targets=validation_targets)
