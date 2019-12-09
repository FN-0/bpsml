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
  """ 现有返回信息，仅提示用 """
  ret_collection = {
    '0': '成功',
    '1': '文件格式错误，仅支持"csv"、"xlsx"、"xls"格式',
    '2': '文件数据读取错误: ',
    '3': '文件内出现英文字符: ',
    '4': '存在重复基因',
    '5': '缺少必须基因',
    '6': '读取基因列表错误，可能存在非基因字符串'
  }
  ftype = is_csv_or_excl(sys.argv[1])
  df, ret_code, msg = read_data(ftype)
  file_path = 'SVM/data/Std_gene_id.txt'
  check_data_file = os.path.exists(file_path)
  if ret_code == 0 and check_data_file:
    with open(file_path, 'r') as fsgenes:
      std_genes = read_gene_from_file(fsgenes)
      df_data_pos_type = locate_genes_and_data_pos(df, df_data_pos_types)
      df_type = df_data_pos_types.index(df_data_pos_type)
      (gid_index, ret_code, msg) = check_gene_id(df, std_genes, df_type)
      if ret_code == 0:
        (data_list, header, ret_code, msg) = check_data(df, df_type)
        if ret_code == 0:
          selected = take_selected_data(df_type, data_list, gid_index)
          return (data_transposer(selected), header, ret_code, msg)
  
  return (None, None, ret_code, msg)

def main():
  try:
    (input_data, header, code, msg) = check_input()
  except TypeError as err:
    print(err)
    return

  """ 读取Model """
  jsondata = None
  if code == 0:
    with open('save/svc_20191202_111229.pickle', 'rb') as f:
        clf = pickle.load(f)
        #测试读取后的Model
        y_predict = clf.predict(input_data)
          
        if header:
          data = dict(zip(header, y_predict))
        else:
          data = dict(zip([x for x in range(0, len(y_predict))], y_predict))

        jsondata = json.dumps(data, ensure_ascii=False)
        #print(jsondata)
      
  """ json构成 """
  jdict = {"code": code, "msg": msg, "data": jsondata}
  jsonout = json.dumps(jdict, ensure_ascii=False)
  print(jsonout)

if __name__ == "__main__":
  main()
