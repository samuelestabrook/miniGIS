from Feature import *
from Commons import *

class Point(Feature):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def dis(self,ep):
	return math.sqrt((self.x-ep.x)**2+(self.y-ep.y)**2)
    def vis(self, map, color):
	self.transform(map)
	map.can.create_rectangle(self.winx-2, self.winy-2, self.winx+2, self.winy+2, fill=color)
    def transform(self, map):
	self.winx, self.winy = transformX(self.x, map), transformY(self.y, map)

    # Using different color and oval to visualize intersections
    def visInterseccts(self, map, borderColor='red', fillColor='yellow'):
        self.transform(map)
	map.can.create_oval(self.winx-4, self.winy-4, self.winx+4, self.winy+4, outline=borderColor, fill=fillColor, width=1)

        
