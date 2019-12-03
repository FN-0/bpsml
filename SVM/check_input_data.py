# -*- coding: utf-8 -*-
# !/usr/bin/env python

""" 检查输入数据是否符合规则
"""

import os
import sys
import numbers
import pandas as pd

""" 检查基因id的完整性
"""
def check_gene_id(df, std_genes, df_type):
  gid_lst = get_gene_id(df, df_type)
  if gid_lst and not check_duplicates(gid_lst):
    for sg in std_genes:
      if sg not in gid_lst:
        return False
    else:
      return True
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
        return False
    else:
      return True

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

def read_data(ftype, errors):
  try:
    if ftype.lower() == 'csv':
      df = pd.read_csv(sys.argv[1], header=None)
    elif ftype.lower() == 'xlsx':
      df = pd.read_excel(sys.argv[1], header=None)
    elif ftype.lower() == 'xls':
      df = pd.read_excel(sys.argv[1], header=None)
    else:
      return errors[1]
    return df
  except:
    return errors[2]

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
  errors = [
    'Something\'s wrong.',
    'Not support format.',
    'Open failed.'
  ]
  df_data_pos_types = [
    'left_without_header',
    'top_without_header',
    'left_with_header',
    'top_with_header'
  ]
  ftype = is_csv_or_excl(sys.argv[1])
  df = read_data(ftype, errors)
  file_path = '.\SVM\Std_gene_id.txt'
  if os.path.exists(file_path):
    with open(file_path, 'r') as fsgenes:
      std_genes = read_gene_from_file(fsgenes)
      if str(df) in errors:
        print(df)
      else:
        df_data_pos_type = locate_genes_and_data_pos(df, df_data_pos_types)
        df_type = df_data_pos_types.index(df_data_pos_type)
        gid_check = check_gene_id(df, std_genes, df_type)
        data_check = check_data(df, df_type)
        if gid_check and data_check:
          print('Done.\nAll Pass.')
        else:
          print('Done.\nSomething wrong with your data.')
  else:
    print(file_path+' does not exist.')

if __name__ == "__main__":
  main()
  