# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pandas as pd

def get_select_gene(df, glst):
  return df.loc[glst]

if __name__ == "__main__":
  df = pd.read_csv(sys.argv[1], index_col='AccID')
  f = open('gene_list.txt', 'r')
  gene_lst = []
  for gid in f.readlines():
    gene_lst.append(gid.strip('\n'))
  df = get_select_gene(df, gene_lst)
  df.to_csv(os.path.basename(sys.argv[1]).split('.')[0]+'_.csv')
