# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import numpy as np
import pandas as pd

def find_n_nonzero_row(df, n):
  n_nonzero_row_list = []
  for label, row in df.iterrows():
    protein_array = np.array(row.to_list())
    if np.count_nonzero(protein_array) == int(n):
      n_nonzero_row_list.append(label)
  return n_nonzero_row_list

def remove_confirm(len_index, len_n_nonzero_row_list):
  print('Length of rest of gene: ', len_index-len_n_nonzero_row_list)
  '''remove_conf = input('Remove? y/n ')
  if remove_conf == 'y':
    return True
  elif remove_conf == 'n':
    pass
  else:
    print('Usage: input y or n.')
  return False'''
  return True

def remove_row(df, n_nonzero_row_list):
  return df.drop(n_nonzero_row_list)

def main():
  df = pd.read_csv(sys.argv[1], encoding = "ISO-8859-1", index_col='AccID')
  print(len(df.index))
  n=int(input('Input number of non zero number.\n'))
  for x in range(0, n+1):
    n_nonzero_row_list = find_n_nonzero_row(df, x)
    print(len(n_nonzero_row_list))
    if remove_confirm(len(df.index), len(n_nonzero_row_list)):
      df = remove_row(df, n_nonzero_row_list)
    else:
      pass
  df.to_csv(os.path.basename(sys.argv[1]).split('.')[0]+'_without_0-'+str(n)+'.csv')

if __name__ == "__main__":
  main()
