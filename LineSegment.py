from Commons import *
from Point import *

class LineSegment:
    # Init the class with the coordinates of the first point and end point
    def __init__(self, startX, startY, endX, endY):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY


    # (X, Y) is a point, detect which side of the Line Segment it is in
    # If the return is 0, the point is on the Line 
    def cross(self, x, y):
        return(self.endX - self.startX)*(y - self.startY) - (x - self.startX)*(self.endY - self.startY);

    # (X, Y) is a point which is on the Line , detect if this point on the Line Segment
    def onSegment(self, x, y):
       return (x - self.startX) * (x - self.endX) <= 0
    
    # Detect if the input Line Segment intersects with 'self'
    def intersectLineseg(self, inputLineSeg):
        # caculate the cross of the first point of the input Line Segment to self
        d1 = self.cross(inputLineSeg.startX, inputLineSeg.startY)
        # caculate the cross of the end point of the input Line Segment to self
        d2 = self.cross(inputLineSeg.endX, inputLineSeg.endY)
        # caculate the cross of the first point of self to the input Line Segment
        d3 = inputLineSeg.cross(self.startX, self.startY)
        # caculate the cross of the end point of self to the input Line Segment
        d4 = inputLineSeg.cross(self.endX, self.endY)

        
        # if the two line segments cross each other, they should intersect
        # It means d1*d2 < 0 and d3*d4 < 0
        if d1*d2 < 0 and d3*d4 < 0:
            self.intersectionX = (inputLineSeg.startX*d2 - inputLineSeg.endX*d1)/(d2 - d1)
            self.intersectionY = (inputLineSeg.startY*d2 - inputLineSeg.endY*d1)/(d2 - d1)
            
            return Point(self.intersectionX, self.intersectionY)
        # If d1 = 0, the first Point of input Line Segement is on the Line, but we should detect if the point is on the Line Segemnt
        elif 0 == d1 and self.onSegment(inputLineSeg.startX, inputLineSeg.startY):
            self.intersectionX = inputLineSeg.startX
            self.intersectionY = inputLineSeg.startY
            return Point(self.intersectionX, self.intersectionY)       
        # If d2 = 0, the end Point of input Line Segement is on the Line, but we should detect if the point is on the Line Segemnt
        elif 0 == d2 and self.onSegment(inputLineSeg.endX, inputLineSeg.endY):
            self.intersectionX = inputLineSeg.endX
            self.intersectionY = inputLineSeg.endY
            return Point(self.intersectionX, self.intersectionY)
        # If d3 = 0, the first Point of self is on the input Line , but we should detect if the point is on the Line Segemnt
        elif 0 == d3 and inputLineSeg.onSegment(self.startX, self.startY):
            self.intersectionX = self.startX
            self.intersectionY = self.startY
            return Point(self.intersectionX, self.intersectionY)
        # If d1 = 0, the end Point of self is on the input Line , but we should detect if the point is on the Line Segemnt
        elif 0 == d4 and inputLineSeg.onSegment(self.endX, self.endY):
            self.intersectionX = self.endX
            self.intersectionY = self.endY
            return Point(self.intersectionX, self.intersectionY)
        # They will not intersect in other cases
        else:
            return None


    def getBBox(self):
        [minX, maxX] = sorted([self.startX, self.endX])
        [minY, maxY] = sorted([self.startY, self.endY])
        return [minX, minY, maxX, maxY]

    def getLength(self):
        return math.sqrt((self.startX-self.endX)**2+(self.startY-self.endY)**2)

    #check if the bbox of linesegment outside of the input bbox
    #this can improve the performance to check if the linesegment intersect with polyline
    def isOutsideOfBBox(self, bBox):
        return checkIsOutside(self.getBBox(), bBox)
