# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import pandas as pd

def get_gene_id(filename):
  df = pd.read_csv(filename, header=0)
  gene_id = df.iloc[:, 0]
  return gene_id

if __name__ == "__main__":
  filename = sys.argv[1]
  gene_id = get_gene_id(filename)
  f = open(os.path.basename(sys.argv[1]).split('.')[0]+'_gid.txt', 'w')
  for gid in gene_id.to_list():
    f.write(str(gid)+'\n')
