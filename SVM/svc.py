# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import pickle
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold, cross_val_score, ShuffleSplit
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

def main():
  df = pd.read_csv(sys.argv[1], header=0)
  x = df.iloc[0:, 0:].to_numpy()
  y = df.iloc[0:, 0].to_numpy()

  """ 拆分训练数据与测试数据 """
  ss = ShuffleSplit(n_splits=4, test_size=0.3)
  for train_index, test_index in ss.split(x):
    x_train, y_train = x[train_index], y[train_index]
    x_test, y_test = x[test_index], y[test_index]
    lsvc = svm.SVC(kernel='linear', C=1).fit(x_train, y_train)
  
    """ 输出分类结果 """
    y_predict = lsvc.predict(x_test)
    score = lsvc.score(x_test, y_test)
    cr = classification_report(y_test, y_predict)
    print('The Accuracy of LinearSVC is:', score)
    print(cr)

    """ 保存Model """
    is_save = input('Sava this model? y/n ')
    if is_save == 'y':
      with open('save/lsvc_'+str(score)+'.pickle', 'wb') as f:
        pickle.dump(lsvc, f)
      with open('save/lsvc_'+str(score)+'.txt', 'w') as f:
        f.write(cr)
    elif is_save == 'n':
      pass
    else:
      return

if __name__ == "__main__":
  main()
