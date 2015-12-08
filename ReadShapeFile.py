import struct
from Layer import *
from Point import *
from Polyline import *
from Polygon import *

def readShpPoint(layer,fileName): # parameter fileName is the pathfile name without extension
    fileName = fileName + '.shp'
    shpFile=open(fileName,'rb')
    s = shpFile.seek(24)
    s = shpFile.read(4)
    b = struct.unpack('>i',s)
    featNum = (b[0]*2-100)/28
    s = shpFile.read(72)
    header = struct.unpack("<iidddddddd",s)
    layer.minx, layer.miny, layer.maxx, layer.maxy = header[2],header[3],header[4],header[5]
    for i in range(0,featNum):
        
        shpFile.seek(100+12+i*28)
        s = shpFile.read(16)
        x,y = struct.unpack('dd',s)
        point = Point(x,y)
        layer.features.append(point)
    shpFile.close()

# read .shx file firstly
# then read shape file
# polyline and polygon file are similar, so use this to read both polyline and polygon
def readShpPoly(layer,fileName, layerType):# parameter fileName is the pathfile name without extension
    indexName = fileName+'.shx'
    shxFile = open(indexName,"rb")
    s = shxFile.read(28)
    header = struct.unpack(">iiiiiii",s)
    fileLength = header[len(header)-1]
    polylineNum = (fileLength*2-100)/8
    s = shxFile.read(72)
    header = struct.unpack("<iidddddddd",s)
    layer.minx, layer.miny, layer.maxx, layer.maxy = header[2],header[3],header[4],header[5]
    recordsOffset = []
    for i in range(0,polylineNum):
        shxFile.seek(100+i*8)
        s = shxFile.read(4)
        offset = struct.unpack('>i',s)
        recordsOffset.append(offset[0]*2)
    shxFile.close()

    shpFile = open(fileName+'.shp',"rb")
    for offset in recordsOffset:
        x, y = [], []
        shpFile.seek(offset+8+4)
        
        feature = Polyline() if 3 == layerType else Polygon()
        s = shpFile.read(32)
        minx, miny, maxx, maxy = struct.unpack('dddd',s)
        feature.setBBox(minx, miny, maxx, maxy)
        
        s = shpFile.read(8)
        feature.numParts, feature.numPoints = struct.unpack('ii',s)
        s = shpFile.read(4*feature.numParts)
        str = ''
        for i in range(feature.numParts):
            str = str+'i'
        feature.partsIndex = struct.unpack(str,s)
        for i in range(feature.numPoints):
            s = shpFile.read(16)
            pointx, pointy = struct.unpack('dd',s)
            x.append(pointx)
            y.append(pointy)
        feature.setCoordinates(x, y)
        layer.features.append(feature)
    shpFile.close()


     
