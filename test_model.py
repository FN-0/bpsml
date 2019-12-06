# -*- coding:utf-8 -*-
# !/usr/bin/env python

import os
import sys
import json
import pickle
from collections import Counter
from SVM.check_input_data import check_gene_id, check_data, is_csv_or_excl
from SVM.check_input_data import locate_genes_and_data_pos, take_selected_data
from SVM.check_input_data import read_data, read_gene_from_file, data_transposer

def check_input():
  df_data_pos_types = [
    'gene_at_left_without_header',
    'gene_at_top_without_header',
    'gene_at_left_with_header',
    'gene_at_top_with_header'
  ]
  ftype = is_csv_or_excl(sys.argv[1])
  df = read_data(ftype)
  file_path = 'SVM/data/Std_gene_id.txt'
  check_data_file = os.path.exists(file_path)
  if not df.empty and check_data_file:
    with open(file_path, 'r') as fsgenes:
      std_genes = read_gene_from_file(fsgenes)
      df_data_pos_type = locate_genes_and_data_pos(df, df_data_pos_types)
      df_type = df_data_pos_types.index(df_data_pos_type)
      #print(df_type)
      gid_index = check_gene_id(df, std_genes, df_type)
      (data_list, header) = check_data(df, df_type)
      if gid_index and data_list:
        selected = take_selected_data(df_type, data_list, gid_index)
        return (data_transposer(selected), header)
      else:
        print('illegal value.')
  else:
    if not check_data_file:
      print(file_path+' does not exist.')

def make_report(y_predict):
  pass

def main():
  try:
    (input_data, header) = check_input()
  except TypeError as err:
    print(err)
    return

  """ 读取Model """
  with open('save/svc_20191202_111229.pickle', 'rb') as f:
      clf = pickle.load(f)
      #测试读取后的Model
      y_predict = clf.predict(input_data)
        
      if header:
        out = dict(zip(header, y_predict))
      else:
        out = dict(zip([x for x in range(0, len(y_predict))], y_predict))

      jsonout = json.dumps(out, ensure_ascii=False)
      print(jsonout)
      
      count = Counter(y_predict)
      for c in count:
        print(c, count[c])

if __name__ == "__main__":
  main()
