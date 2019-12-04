# -*- coding: utf-8 -*-
# !/usr/bin/env python

""" 检查输入数据是否符合规则
"""

import os
import sys
import ast
import numbers
import pandas as pd

""" 检查基因id的完整性
"""
def check_gene_id(df, std_genes, df_type):
  gid_lst = get_gene_id(df, df_type)
  if check_duplicates(gid_lst):
    print('存在重复基因')
    return False
  if gid_lst:
    index = []
    for sg in std_genes:
      if sg not in gid_lst:
        return False
      else:
        index.append(gid_lst.index(sg))
    else:
      return index
  else:
    return False

""" 检查数据格式
"""
def check_data(df, df_type):
  if df_type == 0:
    data = df.iloc[:, 1:].values.tolist()
  elif df_type == 1:
    data = df.iloc[1:, :].values.tolist()
  elif df_type == 2:
    data = df.iloc[1:, 1:].values.tolist()
  elif df_type == 3:
    data = df.iloc[1:, 1:].values.tolist()
  
  for row in data:
    for e in row:
      if not isinstance(e, numbers.Number):
        try:
          row[row.index(e)] = ast.literal_eval(e)
        except ValueError as err:
          print('文件内出现非数字字符' ,err)
          return False
    else:
      return data

""" 从通过检查的数据中获取需要的数据
"""
def take_selected_data(data_list, gid_index, std_genes):
  selected = []
  for index in gid_index:
    selected.append(data_list[index])
  return selected

def data_transposer(df_type, data_list):
  if df_type == 0 or df_type == 2:
    return list(map(list, zip(*data_list)))
  else:
    return data_list


""" 检查基因列表是否重复
"""
def check_duplicates(lst):
  return len(lst) != len(set(lst))

def read_gene_from_file(f):
  gene_lst = []
  for gid in f.readlines():
    gene_lst.append(gid.strip('\n'))
  return gene_lst

def is_csv_or_excl(f):
  last = os.path.basename(f).split('.')[1]
  return last

""" 根据文件后缀读取文件内数据，可扩展
"""
def read_data(ftype):
  try:
    if ftype.lower() == 'csv':
      df = pd.read_csv(sys.argv[1], header=None)
    elif ftype.lower() == 'xlsx':
      df = pd.read_excel(sys.argv[1], header=None)
    elif ftype.lower() == 'xls':
      df = pd.read_excel(sys.argv[1], header=None)
    else:
      print('文件格式错误')
    return df
  except Exception as exc:
    print('文件数据读取错误', exc)

def is_gene_id(s):
  return len(s) == 15 and (s[0:4].lower() == 'ensg')

def locate_genes_and_data_pos(df, df_types):
  first_item = df.iloc[0, 0]
  if is_gene_id(first_item):
    if is_gene_id(df.iloc[1, 0]):
      return df_types[0]
    elif is_gene_id(df.iloc[0, 1]):
      return df_types[1]
  else:
    if is_gene_id(df.iloc[1, 0]):
      return df_types[2]
    elif is_gene_id(df.iloc[0,1]):
      return df_types[3]
  
def get_gene_id(df, df_type):
  if df_type == 0:
    gid = df.iloc[:, 0].to_list()
  elif df_type == 1:
    gid = df.iloc[0, :].to_list()
  elif df_type == 2:
    gid = df.iloc[1:, 0].to_list()
  elif df_type == 3:
    gid = df.iloc[0, 1:].to_list()

  if gid:
    for g in gid:
      if not is_gene_id(g):
        break
    else:
      return gid

def main():
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
          print('All Pass.')
          selected = take_selected_data(data_list, gid_index, std_genes)
          return data_transposer(df_type, selected)
        else:
          print('illegal value.')
  else:
    print(file_path+' does not exist.')

if __name__ == "__main__":
  main()
  