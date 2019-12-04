#! PYTHONEXE
import sys
sys.path = ["/Users/Qianshu/Downloads/code/plc_3.0/plc-3.01/lib/python/site-packages"]+sys.path

import numpy as nm
import clik

def main(argv):
  if clik.try_lensing(argv[1]):
    main_lensing(argv)
    return 
  main_CMB(argv)

def main_CMB(argv):
  lklfile = argv[1]
  lkl = clik.clik(lklfile)
  for clfile in argv[2:]:
    cls = nm.loadtxt(clfile)
    nres = lkl(cls.flat[:])
    print(nres)

def main_lensing(argv):
  lklfile = argv[1]
  lkl = clik.clik_lensing(lklfile)
  print("lensed\n")
  for clfile in argv[2:]:
    cls = nm.loadtxt(clfile)
    nres = lkl(cls.flat[:])
    print(nres)

if __name__=="__main__":
    lklfile = './plik'
    lkl = clik.clik(lklfile)
    cls = nm.loadtxt('data.txt')
    cls2 = nm.loadtxt('data2.txt')
    print(lkl(cls.flat[:])[0])
    print(lkl(cls2.flat[:])[0])