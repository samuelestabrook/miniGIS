from ReadShapeFile import *
import struct

class Layer:
    def __init__(self, fileName, color):
        self.features = []
        self.loadData(fileName, color)
        self.fileName = fileName
        self.color = color

    # load the shape data
    # read .shx file to get the layer type firstly
    # then read the coordinates in shape file
    def loadData(self,fileName,color):
        shpFile = open(fileName+'.shx',"rb")
        shpFile.seek(32)
        s = shpFile.read(4)
        shapeType, = struct.unpack("i",s)
        layer = 0;
        if shapeType==1:
            self.shapeType = 1
            readShpPoint(self,fileName)
        elif shapeType == 3:
            self.shapeType = 3
            readShpPoly(self,fileName,3)
        elif shapeType == 5:
            self.shapeType = 5
            readShpPoly(self,fileName,5)
        else:
            print 'not a valid shape file' + str(shapeType)
            return 0

    #return the shape file name
    def getFileName(self):
        return self.fileName

    #check the intersects between two polyline layers
    #if one or two of them are not polyline layer, return None
    def checkIntersects(self, layer):
        if(self.shapeType != 3 or layer.shapeType != 3):
            return None
        # if the boundingboxs don't have overlap, sure, they do not have intersects
        if(self.minx > layer.maxx or self.maxx < layer.minx or self.miny > layer.maxy or self.maxx < layer.miny):
            return None
        intersects = []

        for feature in self.features:
            tempIntersects = feature.intersectLayer(layer)
            if (tempIntersects == None or tempIntersects == []):
                continue
            for intersect in tempIntersects:
                intersects.append(intersect)
            
        return intersects

    # visualize the layer using color
    def vis(self, map):
        for feature in self.features:
            feature.vis(map, self.color)

