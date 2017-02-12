#!/bin/env python

from PySBIG import PySBIG
import numpy
import sys

fileName = sys.argv[1]

sbig = PySBIG(fileName)

print sbig.getHeaders()
data = sbig.getData()
print data.shape
print len(data[1])
print data.max()
print data.min()
#print data

