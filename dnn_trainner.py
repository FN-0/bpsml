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

def construct_feature_columns(input_features):
  return set([tf.feature_column.numeric_column(my_features)
              for my_features in input_features])

def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
  features = {key:np.array(value) for key,value in dict(features).items()}

  ds = Dataset.from_tensor_slices((features, targets))
  ds = ds.batch(batch_size).repeat(num_epochs)

  if shuffle:
      ds = ds.shuffle(buffer_size=200)

  features, labels = ds.make_one_shot_iterator().get_next()
  return features, labels

def train_nn_classification_model(
    learning_rate,
    l1_regularization_strength,
    l2_regularization_strength,
    steps,
    batch_size,
    hidden_units,
    training_examples,
    training_targets,
    validation_examples,
    validation_targets):

  periods = 10
  steps_per_period = steps / periods
  # Model save path
  dir_path = os.path.dirname(os.path.realpath(__file__))
  models_path=os.path.join(dir_path,'models/'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'/')
  # Create a DNNRegressor object.
  my_optimizer = tf.train.FtrlOptimizer(
                   learning_rate=learning_rate, 
                   l1_regularization_strength=l1_regularization_strength, 
                   l2_regularization_strength=l2_regularization_strength)
  my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  classifier = tf.estimator.DNNClassifier(
      feature_columns=construct_feature_columns(training_examples),
      n_classes=3,
      hidden_units=hidden_units,
      optimizer=my_optimizer,
      config=tf.contrib.learn.RunConfig(keep_checkpoint_max=1),
      model_dir=models_path
  )
  
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

  # Train the model, but do so inside a loop so that we can periodically assess
  # loss metrics.
  print("Training model...")
  print("Accuracy:")
  training_errors = []
  validation_errors = []
  for period in range (0, periods):
    # Train the model, starting from the prior state.
    classifier.train(
        input_fn=training_input_fn,
        steps=steps_per_period
    )
    # Take a break and compute predictions.
    training_predictions = list(classifier.predict(input_fn=predict_training_input_fn))
    training_probabilities = np.array([item['probabilities'] for item in training_predictions])
    training_pred_class_id = np.array([item['class_ids'][0] for item in training_predictions])
    training_pred_one_hot = tf.keras.utils.to_categorical(training_pred_class_id, 3)
    #training_predictions = np.around(training_predictions)
    
    validation_predictions = list(classifier.predict(input_fn=predict_validation_input_fn))
    validation_probabilities = np.array([item['probabilities'] for item in validation_predictions])    
    validation_pred_class_id = np.array([item['class_ids'][0] for item in validation_predictions])
    validation_pred_one_hot = tf.keras.utils.to_categorical(validation_pred_class_id, 3)
    #validation_predictions = np.around(validation_predictions)
    
    # Compute training and validation errors.
    training_log_loss = metrics.log_loss(training_targets, training_pred_one_hot)
    validation_log_loss = metrics.log_loss(validation_targets, validation_pred_one_hot)
    # Occasionally print the current loss.
    print("  period %02d : %0.2f %0.2f" % (period, training_log_loss, validation_log_loss))
    # Add the loss metrics from this period to our list.
    training_errors.append(training_log_loss)
    validation_errors.append(validation_log_loss)
  print("Model training finished.")

  # Remove event files to save disk space.
  #_ = map(os.remove, glob.glob(os.path.join(classifier.model_dir, 'events.out.tfevents*')))
  
  # Calculate final predictions (not probabilities, as above).
  final_predictions = classifier.predict(input_fn=predict_validation_input_fn)
  final_predictions = np.array([item['class_ids'][0] for item in final_predictions])
  
  accuracy = metrics.accuracy_score(validation_targets, final_predictions)
  print("Final accuracy (on validation data): %0.2f" % accuracy)

  # Output a graph of loss metrics over periods.
  plt.ylabel("LogLoss")
  plt.xlabel("Periods")
  plt.title("LogLoss vs. Periods")
  plt.plot(training_errors, label="training")
  plt.plot(validation_errors, label="validation")
  plt.legend()
  plt.savefig(os.path.join(models_path, "%0.0f.png" % (accuracy*100)))
  plt.show()
  
  return classifier

if __name__ == '__main__':
  #tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
  gene_df = pd.read_csv('ready2train/'+sys.argv[1]+'.csv', header=0)
  gene_df = gene_df.reindex(np.random.permutation(gene_df.index))
  training_examples = gene_df.drop('Label', axis=1).head(170)
  training_targets = gene_df['Label'].head(170)
  validation_examples = gene_df.drop('Label', axis=1).tail(53)
  validation_targets = gene_df['Label'].tail(53)
  classifier = train_nn_classification_model(
      learning_rate=0.0001,
      l1_regularization_strength=0.1,
      l2_regularization_strength=0.1,
      steps=1500,
      batch_size=40,
      hidden_units=[30, 50, 50, 30],
      training_examples=training_examples,
      training_targets=training_targets,
      validation_examples=validation_examples,
      validation_targets=validation_targets)
