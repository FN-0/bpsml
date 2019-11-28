# -*- coding: utf-8 -*-
# !/usr/bin/env python

import sys
import pandas as pd
from os import listdir
from os.path import isfile, join

def transpose(filenames):
  outfile_names = []
  for filename in filenames:
    df = pd.read_csv(filename, header=None)
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0)).reset_index(drop=True)
    outfile_name = '_transpose.'.join(filename.split('.'))
    outfile_names.append(outfile_name)
    df_t = df.T
    df_t.to_csv(outfile_name, header=None)
  return outfile_names

if __name__ == "__main__":
  #onlyfiles = [f for f in listdir('.\\ready2train') if isfile(join('.\\ready2train', f))]
  of = transpose([sys.argv[1]])
