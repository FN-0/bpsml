# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import pickle
import pandas as pd
from sklearn import svm
from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef[0]
    imp, names = zip(*sorted(list(zip(imp, names))))

    # Show all features
    if top == -1:
      top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top], rotation=20, size='x-small')
    plt.show()

def main():
  n_class = 2
  df = pd.read_csv(sys.argv[1])#.fillna(0)
  features_names = list(df)[1:]
  f = open('save/84_202002271629_2c/svc_20200227_162928.pickle', 'rb')
  lsvc = pickle.load(f)
  f_importances(lsvc.coef_, features_names, top=-1)

if __name__ == "__main__":
  main()
