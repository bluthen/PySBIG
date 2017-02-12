#!/bin/env python

from cPySBIG import cPySBIG
import numpy 
import sys

fileName = sys.argv[1]

sbig = cPySBIG(fileName)

print sbig.getHeaders()
data = sbig.getData()
print data.shape
print len(data[1])
print data.max()
print data.min()
#print data
