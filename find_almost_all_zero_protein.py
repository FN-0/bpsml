# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pandas as pd

def find_almost_all_zero_row(df):
  for label, row in df.iterrows():
    print('label:', label)
    print('row:', row.to_list())
    input()

if __name__ == "__main__":
  df = pd.read_csv(sys.argv[1], index_col='Mark')
  find_almost_all_zero_row(df)
