# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pandas as pd

def get_data_from_fd(fn):
  df = pd.read_excel(fn, header=0, index_col=0)
  print(df)
  #key = input()
  f = open('missing_gene_id.txt', 'r')
  gid_lst = []
  for gid in f.readlines():
    gid_lst.append(gid.strip('\n'))
  protein_coding = df.loc[gid_lst, :]
  return protein_coding

if __name__ == "__main__":
  protein_coding = get_data_from_fd(sys.argv[1])
  ocsv = os.path.basename(sys.argv[1]).split('.')[0]
  protein_coding.to_csv(ocsv+'_protein.csv')
