# -*- coding:utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pickle
import numpy as np
from sklearn.metrics import classification_report
from check_input_data import data_transposer
from check_input_data import read_data, read_gene_from_file
from check_input_data import check_gene_id, check_data, is_csv_or_excl
from check_input_data import locate_genes_and_data_pos, take_selected_data

def check_input():
  df_data_pos_types = [
    'left_without_header',
    'top_without_header',
    'left_with_header',
    'top_with_header'
  ]
  ftype = is_csv_or_excl(sys.argv[1])
  df = read_data(ftype)
  file_path = '.\SVM\Std_gene_id.txt'
  if os.path.exists(file_path):
    with open(file_path, 'r') as fsgenes:
      std_genes = read_gene_from_file(fsgenes)
      if str(df):
        df_data_pos_type = locate_genes_and_data_pos(df, df_data_pos_types)
        df_type = df_data_pos_types.index(df_data_pos_type)
        gid_index = check_gene_id(df, std_genes, df_type)
        data_list = check_data(df, df_type)
        if gid_index and data_list:
          selected = take_selected_data(data_list, gid_index, std_genes)
          return data_transposer(df_type, selected)
        else:
          print('illegal value.')
  else:
    print(file_path+' does not exist.')

def main():
  input_data = check_input()

  """ 读取Model """
  with open('save/svc_20191202_111229.pickle', 'rb') as f:
      clf2 = pickle.load(f)
      #测试读取后的Model
      y_predict = clf2.predict(input_data)
      print(y_predict)

if __name__ == "__main__":
  main()
