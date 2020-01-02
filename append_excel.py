# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pandas as pd

def merge_2_df(e1, e2):
  return e1.merge(e2, on='AccID', how='left')

if __name__ == "__main__":
  df1 = pd.read_excel(sys.argv[1])
  df2 = pd.read_excel(sys.argv[2])
  dfa = merge_2_df(df1, df2)
  dfn1 = os.path.basename(sys.argv[1]).split('.')[0]
  dfn2 = os.path.basename(sys.argv[2]).split('.')[0]
  dfa.to_excel(dfn1+'+'+dfn2+'.xlsx', index=0)
