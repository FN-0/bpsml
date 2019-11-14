# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pandas as pd

def remove_extra_gene(df, exg_lst):
  return df.drop(exg_lst)

if __name__ == "__main__":
  df = pd.read_csv(sys.argv[1], index_col='AccID')
  f = open('missing_gene_id.txt', 'r')
  exg_lst = []
  for gid in f.readlines():
    exg_lst.append(gid.strip('\n'))
  df = remove_extra_gene(df, exg_lst)
  df.to_csv(os.path.basename(sys.argv[1]).split('.')[0]+'_43249.csv')
