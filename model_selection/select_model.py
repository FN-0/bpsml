# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn import tree
from sklearn import neural_network
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

def main():
  df = pd.read_csv(sys.argv[1], header=0)
  x = df.iloc[0:184, 1:].to_numpy()
  y = df.iloc[0:184, 0].to_numpy()

  svmclf = svm.SVC(kernel='linear', C=1)
  dctclf = tree.DecisionTreeClassifier()
  extclf = tree.ExtraTreeClassifier()
  mlpclf = neural_network.MLPClassifier()
  gnbclf = GaussianNB()
  sgdclf = SGDClassifier()

  clf_lst = [svmclf, dctclf, extclf, mlpclf, gnbclf, sgdclf]

  cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)

  """ 输出分类结果 """
  for clf in clf_lst:
    scores = cross_val_score(clf, x, y, cv=cv, scoring='recall')
    print(scores)

if __name__ == "__main__":
  main()
