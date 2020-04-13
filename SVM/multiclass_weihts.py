# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import pickle
import numpy as np
import pandas as pd
from sklearn import svm
from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    #imp = coef
    top_positive_coefficients = np.argsort(coef)[-top:]
    top_negative_coefficients = np.argsort(coef)[:top]
    print(top_negative_coefficients)
    print(top_positive_coefficients)
    imp = np.append(top_negative_coefficients, top_positive_coefficients)
    imp, names = zip(*sorted(list(zip(imp, names))))

    # Show all features
    if top == -1:
      top = len(names)

    plt.barh(range(top*2), imp[::-1][0:top*2], align='center')
    plt.yticks(range(top*2), names[::-1][0:top*2])
    plt.show()           

def main():
  n_class = 2
  df = pd.read_csv(sys.argv[1])#.fillna(0)
  features_names = list(df)[1:]
  f = open('save/145gene_202003020848/svc_20200302_084801.pickle', 'rb')
  lsvc = pickle.load(f)
  for coef in lsvc.coef_:
    f_importances(coef, features_names, top=10)

if __name__ == "__main__":
  main()
