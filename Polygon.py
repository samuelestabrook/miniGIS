from Polyline import *
from Point import *
import shapefile

#  polyline class has many functions could be used in polygon class
class Polygon(Polyline):
    def __init__(self):
        pass
        
    def vis(self,map, color):
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
	    map.can.create_polygon(tempXYlist, fill=color, outline = 'brown')

    # check if a point is inside the inputPolygon
    #
    # THIS IS THE FUNCTION THAT RETURNS A SET OF POINTS TO VISUALIZE!
    #
    def contain(self, inputPoint):
        intxns = []    # intersections/points contained
        testTrue = self.pip(inputPoint.x, inputPoint.y)
        print testTrue
        print str(self)
        if testTrue:
            intxn = Point(inputPoint.x, inputPoint.y)
            intxns.append(intxn)
        return intxns

    def pip(self, x, y):
#        pts = self.getPoints()
#        n = len(self.points)
        print n
        inside = False
#        for i in range(len(self.points)):
#            print str(self.points[i])
        p1x,p1y = self[0].x,self[0].y
        for pt in self.points:
            p2x,p2y = pt.x,pt.y
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xints:
                                inside = not inside
            p1x,p1y = p2x,p2y
        return inside

#    def getPoints(self):
#        points = []
#        for i in range(self.numParts):
#            
#            x = self.x
#            print str(x)
#            y = self.y
#            print str(y)
#            points.append(Point(x,y))
#        return points

    # check if the polygon contains a point
    def containLayer(self, layer):
        if self.isOutsideOfBBox([layer.minx, layer.miny, layer.maxx, layer.maxy]):
            return None
        intxnSet = []
        for feature in layer.features:
            intxns = self.contain(feature)
            if None == intxns:
                continue
            for intxn in intxns:
                intxnSet.append(intxn)
        return intxnSet
