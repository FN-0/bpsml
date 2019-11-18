# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve  
from sklearn.metrics import classification_report 
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import label_binarize

def main():
  df = pd.read_csv(sys.argv[1], header=0)
  x = df.iloc[0:, 0:]
  y = df.iloc[0:, 0]
  y = label_binarize(y, classes=[0, 1, 2])

  ''''' 拆分训练数据与测试数据 ''' 
  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

  ''''' 使用信息熵作为划分标准，对决策树进行训练 '''  
  clf = tree.DecisionTreeClassifier(criterion='entropy')
  print(clf)
  clf.fit(x_train, y_train)

  ''''' 把决策树结构写入文件 '''  
  with open("tree.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

  ''''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''  
  print('系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大')
  print(clf.feature_importances_)
  for im in clf.feature_importances_:
    print(im)
    input()

  '''''测试结果的打印'''  
  print('测试结果的打印')
  answer = clf.predict(x_train)
  print('np.mean(answer == y_train): \n', np.mean(answer == y_train))
  input()

  '''''准确率与召回率'''  
  #precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))  
  #answer = clf.predict_proba(x.to_numpy)[:,1]  
  #print(classification_report(y, answer, target_names = ['yes', 'no']))
  answer = clf.predict(x_test)
  print('np.mean(answer == y_test): \n', np.mean(answer == y_test))
  
  print(clf.score(x_train, y_train))  # 精度
  print('训练集准确率：', accuracy_score(y_train, clf.predict(x_train)))
  print(clf.score(x_test, y_test))
  print('测试集准确率：', accuracy_score(y_test, clf.predict(x_test)))

if __name__ == "__main__":
  main()
