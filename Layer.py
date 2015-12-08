from ReadShapeFile import *
import struct

class Layer:
    def __init__(self, fileName, color, points=[]):
        self.points = points
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

    # check if the points are inside the polygon layer
    # if there are no point or polygon layers, return None
    def checkContains(self, layer):
        print "self shapeType is " + str(self.shapeType)
        print "layer shapeType is " + str(layer.shapeType)
        if(self.shapeType != 5 or layer.shapeType != 1):
            return None
        # if the bounding bxes don't overlap, they do not intersect either
        if(self.minx > layer.maxx or self.maxx < layer.minx or self.miny > layer.maxy or self.maxx < layer.miny):
            return None
        contains = []

        for feature in self.features:
            print 'selecting polygon'

            # containLayer is in Polygon.py
            tempContains = feature.containLayer(layer)
            if (tempContains == None or tempContains == []):
                continue
            for contain in tempContains:
                print str(contain)
                #
                #
                contains.append(contain)
            
        return contains

    # visualize the layer using color
    def vis(self, map):
        for feature in self.features:
            feature.vis(map, self.color)

