from Feature import *
from LineSegment import *
from Commons import *

import math 
class Polyline(Feature):
    def __init__(self):
        pass
    
    #Considering it may contain multiparts    
    def getLength(self):
        length = 0
        for lineSeg in self.getLineSegs():
            length += lineSeg.getLength()
        return length

    def transform(self, map):
        self.winx, self.winy=[],[]
        for j in range(self.numPoints):
            self.winx.append(transformX(self.x[j], map))
            self.winy.append(transformY(self.y[j], map))

    # this function can be used to visualize multiparts polyline
    # should run transform(map) first then vis(map)
    def vis(self,map,color):
        self.transform(map)
        for k in range(self.numParts):
            if (k==self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[k+1]
            tempXYlist = []
            for m in range(self.partsIndex[k], endPointIndex):
                tempXYlist.append(self.winx[m])
                tempXYlist.append(self.winy[m])
            map.can.create_line(tempXYlist, fill=color, width="2")#map.color
            
    #return the list of the lineSegments in each part in the      
    def getLineSegs(self):
        lineSegs = []
        for i in range(self.numParts):
            if (i == self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[i+1]
            for j in range(self.partsIndex[i], endPointIndex - 1):
                lineSeg = LineSegment(self.x[j], self.y[j], self.x[j+1], self.y[j+1])
                lineSegs.append(lineSeg)
        return lineSegs

    # check if the polyline is outside of bBox
    # it can save time to check the intersections
    # if it is outside of the bBox, return true
    def isOutsideOfBBox(self, bBox):
        return checkIsOutside(self.getBBox(), bBox)

    # check if this polyline intersects inputPolyline
    # if they intersect, return a list containing the intersections
    # return none means this polyline is outside of the bBox of the inputPolyline
    # return empty list means no intersections
    def intersect(self, inputPolyline):
        if self.isOutsideOfBBox(inputPolyline.getBBox()):
            return None
        intxns = []    # intersections 
        for lineSeg in self.getLineSegs():           
            if lineSeg.isOutsideOfBBox(inputPolyline.getBBox()):
                continue          
            for inputLineSeg in inputPolyline.getLineSegs():
                intxn = lineSeg.intersectLineseg(inputLineSeg)
                if intxn != None:
                    intxns.append(intxn)
        return intxns

    # check if the polyline intersects layer
    def intersectLayer(self, layer):
        if self.isOutsideOfBBox([layer.minx, layer.miny, layer.maxx, layer.maxy]):
            return None
        intxnSet = []
        for feature in layer.features:
            intxns = self.intersect(feature)
            if None == intxns:
                continue
            for intxn in intxns:
                intxnSet.append(intxn)
        return intxnSet
            


