# -*- coding: utf-8 -*-
# !/usr/bin/env python

""" 检查输入数据是否符合规则
"""

import os
import sys
import pandas as pd

""" 检查基因id的完整性
"""
def check_gene_id(df):
  fgenes = open('All_gene_id.txt', 'r')
  all_genes = read_gene_from_file(fgenes)

def check_data():
  pass

def read_gene_from_file(f):
  gene_lst = []
  for gid in f.readlines():
    gene_lst.append(gid.strip('\n'))
  return gene_lst

def is_csv_or_excl(f):
  last = os.path.basename(f).split('.')[1]
  return last

def main():
  ftype = is_csv_or_excl(sys.argv[1])
  print(ftype)
  #df = pd.read_csv(sys.argv[1])
  #check_gene_id(df)

if __name__ == "__main__":
  main()
  