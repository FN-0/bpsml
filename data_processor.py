# -*- coding: utf-8 -*-
# !/usr/bin/env python

import pandas as pd
import sys
from show_process import ShowProcess

def transpose(filenames):
  outfile_names = []
  for filename in filenames:
    df = pd.read_csv('data/'+filename, header=0)
    outfile_name = '_transpose.'.join(filename.split('.'))
    outfile_names.append(outfile_name)
    df_t = df.T
    df_t.to_csv('data/'+outfile_name, index=0, header=0)
  return outfile_names

def create_label(filenames):
  label_name = filenames[0].split('_')[0]
  label_array = []
  columns_count = len(pd.read_csv('data/'+filenames[0], header=0).index)
  for _ in range(columns_count):
      label_array.append(1)
  for filename in filenames[1:]:
    row = len(pd.read_csv('data/'+filename, header=0).index)
    columns_count += row
    for _ in range(row):
      label_array.append(0)
  d = {label_name : label_array}
  df = pd.DataFrame(data=d)
  df.to_csv('data/'+label_name+'_label.csv', index=0)
  return label_name+'_label.csv'


def merge_data(label_file_name, filenames):
  label = pd.read_csv('data/'+label_file_name, header=0)
  df = pd.DataFrame()
  for filename in filenames:
    df = df.append(pd.read_csv('data/'+filename, header=0), \
      ignore_index=True, sort=False)
  df = df.fillna(0)
  df = label.join(df, sort=False)
  df.to_csv('data/merged_data.csv', index=0)

def clean_data(filter_standrad=0):
  df = pd.read_csv('data/merged_data.csv', header=0)
  f = open('del_gene.txt', 'w')
  f1 = open('restore_gene.txt', 'w')
  del_count = 0
  max_step = len(df.columns)
  process_bar = ShowProcess(max_step)
  for key, value in df.iteritems():
      process_bar.show_process()
      if len(key) == 15  and value.std() <= filter_standrad:
          f.write(key+'\n')
          df = df.drop(key, axis=1)
          del_count += 1
      else:
          f1.write(key+'\n')
  print(del_count)
  df.to_csv('data/cleaned_data.csv', index=0)
  f.close()
  f1.close()

if __name__=='__main__':
  outfile_names = transpose(sys.argv[1:])
  label_file_name = create_label(outfile_names)
  merge_data(label_file_name, outfile_names)
  clean_data(filter_standrad=100)
