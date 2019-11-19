# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import label_binarize

def main():
  df = pd.read_csv(sys.argv[1], header=0)
  x = df.iloc[0:, 0:]
  y = df.iloc[0:, 0]

  """ 读取Model """
  with open('save/lsvc.pickle', 'rb') as f:
      clf2 = pickle.load(f)
      #测试读取后的Model
      y_predict = clf2.predict(x)
      print(classification_report(y, y_predict, target_names=['出血', '正常', '血栓']))
  
if __name__ == "__main__":
  main()
