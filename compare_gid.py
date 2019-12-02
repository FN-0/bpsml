# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
from show_process import ShowProcess

def compare_lst(src, dst):
  for (s, d) in zip(src, dst):
    if not s == d:
      return (s, d)
  else:
    return 0

def read_gid_from_file(f):
  lst = []
  for gid in f.readlines():
    gid = gid.strip('\n')
    lst.append(gid)
  return lst

def get_difference(src, dst):
  rst = []
  ret = compare_lst(src, dst)
  while not ret == 0:
    rst.append(ret)
    try:
      if ret[0] < ret[1]:
        src.remove(ret[0])
      else:
        dst.remove(ret[1])
    except TypeError:
      print(ret)
    ret = compare_lst(src, dst)
  return rst

def make_outfile_name(fs, fd):
  of_name = ''
  of_name += os.path.basename(fsrc.name).split('.')[0]
  of_name += '_'
  of_name += os.path.basename(fdst.name).split('.')[0]
  of_name += '.txt'
  return of_name
  
if __name__ == "__main__":
  fsrc = open(sys.argv[1], 'r')
  fdst = open(sys.argv[2], 'r')
  src = read_gid_from_file(fsrc)
  dst = read_gid_from_file(fdst)
  print(len(src), len(dst))
  rst = get_difference(src, dst)
  if rst:
    of_name = make_outfile_name(fsrc, fdst)
    of1 = open(of_name, 'w')
    of2 = open('missing_gene_id.txt', 'w')
    for r in rst:
      of1.write(r[0]+','+r[1]+'\n')
      of2.write(r[0]+'\n')
  print('Done.')
  