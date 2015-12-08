class Feature:
    def __init__(self):
        pass
    
    def vis(self,map,color):
        pass

    def setBBox(self, minx, miny, maxx, maxy):
        self.minx, self.miny, self.maxx, self.maxy = minx, miny, maxx, maxy
        
    def getBBox(self):
        return [self.minx, self.miny, self.maxx, self.maxy]

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y
