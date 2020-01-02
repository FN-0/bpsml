# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import pickle
import datetime
import numpy as np
import pandas as pd
from sklearn import neural_network
from sklearn.model_selection import KFold, cross_val_score, ShuffleSplit
from sklearn.metrics import classification_report
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

def main():
  df = pd.read_csv(sys.argv[1])
  features_names = list(df)[1:]
  x = df.iloc[1:, 1:].to_numpy()
  y = df.iloc[1:, 0].to_numpy()

  """ 拆分训练数据与测试数据 """
  ss = ShuffleSplit(n_splits=4, test_size=0.4)
  for train_index, test_index in ss.split(x):
    x_train, y_train = x[train_index], y[train_index]
    x_test, y_test = x[test_index], y[test_index]
    #print(x_train)
    lsvc = neural_network.MLPClassifier().fit(x_train, y_train)
  
    """ 输出分类结果 """
    y_predict = lsvc.predict(x_test)
    score = lsvc.score(x_test, y_test)
    cr = classification_report(y_test, y_predict)
    print('The Accuracy of MLPClassifier is:', score)
    print(cr)

    """ 保存Model """
    is_save = input('Sava this model? y/n ')
    if is_save == 'y':
      with open('save/svc_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.pickle', 'wb') as f:
        pickle.dump(lsvc, f)
      with open('save/svc_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.txt', 'w') as f:
        f.write(cr)
      f_importances(lsvc.coef_, features_names, top=50)
    elif is_save == 'n':
      pass
    else:
      return


if __name__ == "__main__":
  main()
