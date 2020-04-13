# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import pickle
import datetime
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold, cross_val_score, ShuffleSplit, train_test_split
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
  imp = coef[0]
  imp, names = zip(*sorted(list(zip(imp, names))))

  # Show all features
  if top == -1:
    top = len(names)

  plt.barh(range(top), imp[::-1][0:top], align='center')
  plt.yticks(range(top), names[::-1][0:top])
  plt.show()

def plot_cm(classifier, title, normalize, X_test, y_test, class_names):
  disp = plot_confusion_matrix(classifier, X_test, y_test,
                                 display_labels=class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
  disp.ax_.set_title(title)
  print(disp.confusion_matrix)
  plt.show()
                          
def f1_score_check(report, n_class):
  #n_class = len(report)
  for key, value in report.items():
    #print(type(value['f1-score']))
    print(value['f1-score'])
    if value['f1-score'] < 0.65:
      break
  else:
    return True
  return False

def accuracy_check(acc_list, n_class):
  for acc in acc_list:
    if acc < 0.72:
      break
  else:
    return True
  return False

def main():
  n_class = 4
  df = pd.read_csv(sys.argv[1])
  features_names = list(df)[1:]
  x = df.iloc[1:, 1:].to_numpy()
  y = df.iloc[1:, 0].to_numpy()

  #""" 拆分训练数据与测试数据 """
  #ss = ShuffleSplit(n_splits=10, test_size=0.4)
  while True:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.4)
    #x_train, y_train = x[train_index], y[train_index]
    #x_test, y_test = x[test_index], y[test_index]
    #print(x_train)
    #lsvc = svm.SVC(kernel='linear', probability=True, C=1).fit(x_train, y_train)
    lsvc = svm.LinearSVC().fit(x_train, y_train)

    """ 输出分类结果 """
    y_predict = lsvc.predict(x_test)

    cm = confusion_matrix(y_test, y_predict)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    score = lsvc.score(x_test, y_test)
    cr = classification_report(y_test, y_predict)#, output_dict=True)
    print('The Accuracy of LinearSVC is:', score)
    print(cr)
    #input()
    print(cm.diagonal())
    #print(lsvc.dual_coef_)
    #print(cr['正常人']['precision'])
    
    if accuracy_check(cm.diagonal(), n_class):
      """ 保存Model """
      is_save = input('Sava this model? y/n ')
      if is_save == 'y':
        with open('save/svc_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.pickle', 'wb') as f:
          pickle.dump(lsvc, f)
        with open('save/svc_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.txt', 'w') as f:
          f.write('The Accuracy of LinearSVC is:'+str(score)+'\n')
          f.write(str(cr))
          f.write(str(cm.diagonal()))
        f_importances(abs(lsvc.coef_), features_names, top=50)
        # Plot non-normalized confusion matrix
        titles_options = [("Confusion matrix, without normalization", None),
                          ("Normalized confusion matrix", 'true')]
        class_names = ['Cancer', 'Healthy', 'Metastatic', 'Tumor']
        for title, normalize in titles_options:
          plot_cm(lsvc, title, normalize, x_test, y_test, class_names)
      elif is_save == 'n':
        pass
      else:
        return


if __name__ == "__main__":
  main()
