"""
  PySBIG -- A SBIG file python module
  Copyright (C) 2003 Russell E. Valentine

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Coldstone Labs Web Manger; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
import numpy 
import operator
import time
import struct

class PySBIG:
    def __init__(self, filename):
        self.filename = filename
        self.camera = "unknown"
        self.compressed = 0
        
        file = open(self.filename)
        headerContents = file.read(2048)
        
        #Header
        headerList = headerContents.split("\x0a\x0dEnd\x0a\x0d\x1a")[0].split("\x0a\x0d")
        type = headerList.pop(0)        
        self.headerDict = {}
        for value in headerList:
            d = value.split(" = ")
            self.headerDict[d[0]]=d[1]
            
        #Type image
        self.typeInfo = type.split(" ", 1)
        self.camera = self.typeInfo[0]
        if self.typeInfo[1] == "Compressed Image":
            self.compressed=1
        
        height = int(self.headerDict['Height'])
        width = int(self.headerDict['Width'])
    
        dataList = []
        if self.compressed == 1:
#            startTime = time.time()
            for h in range(height):
                t = file.read(2)
                rowLen = struct.unpack('<H', t)[0]
                line = file.read(rowLen)
                if value == (2*width):
                    dataList.append(numpy.fromstring(line, numpy.uint16))
                else:
                    work = []
                    buf = struct.unpack('<H', line[0:2])[0]
                    work.append(buf)
                    at = 2
                    while at != len(line):
                        lineVal = ord(line[at])
                        if lineVal != 128:
                            if lineVal > 128:
                                buf = buf - 256+lineVal
                            else:
                                buf = buf + lineVal
                            work.append(buf)
                            at = at+1
                        else:
                            buf = struct.unpack('<H', line[at+1:at+3])[0]
                            work.append(buf)
                            at = at+3
                    dataList.append(work)
            self.data = numpy.array(dataList, numpy.uint16)
#            print "compressed total time = "+str(time.time()-startTime)+" s"
        elif self.compressed == 0:
            dataString = file.read()
            self.data = numpy.reshape(numpy.fromstring(dataString, numpy.uint16), ( height, width ))
        file.close()

    def getData(self):
        return self.data
    
    def getHeaders(self):
        return self.headerDict;
