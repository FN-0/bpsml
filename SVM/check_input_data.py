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
    return (False, 4, '存在重复基因')
  if gid_lst:
    index = []
    for sg in std_genes:
      if sg not in gid_lst:
        return (False, 5, '缺少必须基因')
      else:
        index.append(gid_lst.index(sg))
    else:
      return (index, 0, '成功')
  else:
    return (False, 6, '读取基因列表错误，可能存在非基因字符串')

""" 检查数据格式
"""
def check_data(df, df_type, n):
  header = None
  if df_type == 0:
    data = df.iloc[:, 1:n+1].values.tolist()
  elif df_type == 1:
    data = df.iloc[1:n+1, :].values.tolist()
  elif df_type == 2:
    data = df.iloc[1:, 1:n+1].values.tolist()
    header = df.iloc[0, 1:n+1].to_list()
  elif df_type == 3:
    data = df.iloc[1:n+1, 1:].values.tolist()
    header = df.iloc[1:n+1, 0].to_list()

  for row in data:
    for e in row:
      if not isinstance(e, numbers.Number):
        try:
          row[row.index(e)] = ast.literal_eval(e)
        except ValueError as err:
          return (False, header, 3, '文件内出现英文字符: '+str(err))
    else:
      return (data, header,  0, '成功')

""" 从通过检查的数据中获取需要的数据
"""
def take_selected_data(df_type, data_list, gid_index):
  selected = []
  if df_type == 1 or df_type == 3:
    data_list = data_transposer(data_list)
  for index in gid_index:
    selected.append(data_list[index])
  return selected

def data_transposer(data_list):
  return list(map(list, zip(*data_list)))


""" 检查基因列表是否重复
"""
def check_duplicates(lst):
  try:
    is_dup = len(lst) != len(set(lst))
    return is_dup
  except:
    return False

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
      return (pd.DataFrame(), 1, '文件格式错误，仅支持"csv"、"xlsx"、"xls"格式')
    return (df, 0, '成功')
  except Exception as err:
    return (pd.DataFrame(), 2, '文件数据读取错误: '+str(err))

def is_gene_id(s):
  try:
    s_len = len(s)
    return (s[0:4].lower() == 'ensg') and s_len == 15
  except:
    return False

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
    'gene_at_left_without_header',
    'gene_at_top_without_header',
    'gene_at_left_with_header',
    'gene_at_top_with_header'
  ]
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

if __name__ == "__main__":
  main()
  