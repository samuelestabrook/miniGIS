# save the events (operations)
from Tkinter import *
from Commons import *

# abstract class for feature draw
class FeatureDraw:
    def __init__(self, can, layer):
        self.can = can
        self.layer = layer
    def point(self, even):
        pass

# class for point draw
class PointDraw(FeatureDraw):
    def __init__(self, can, layer):
        self.can = can
        self.points = []
        spline = 0
        self.can.bind("<Button-1>", self.point)
        self.drawn = None
        self.layer = layer
    def point(self,event):
        self.can.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill=self.layer.color)

# class for polyline draw
class PolylineDraw(FeatureDraw):
    def __init__(self, can, layer):
        self.can = can
        self.points = []
        spline = 0
        self.can.bind("<Button-1>", self.point)
        self.can.bind("<Button-3>", self.graph)
        self.drawn = None
        self.layer = layer
    def point(self,event):
        self.points.append(event.x)
        self.points.append(event.y)
        if self.drawn: self.can.delete(self.drawn)
        if(len(self.points) > 2):
              global theline
              self.create_feature()
        return self.points
    def create_feature(self):
        objectId = self.can.create_line(self.points, tags="theline", fill=self.layer.color, width="2")
        self.drawn = objectId
    def canxy(self,event):
        print event.x, event.y
    def graph(self,event):
        self.points = []
        self.drawn = None

#class for polygon draw
class PolygonDraw(PolylineDraw):
    def create_feature(self):
        objectId = self.can.create_polygon(self.points, tags="thepolygon", fill =self.layer.color)
        self.drawn = objectId

    
trace = 0
# class for circle draw
class CircleDraw: 
    def __init__(self, can, layer):
        canvas = can
        canvas.bind('<ButtonPress-1>', self.onStart)  
        canvas.bind('<B1-Motion>',     self.onGrow)   
        canvas.bind('<ButtonPress-3>', self.onMove)   
        self.canvas = canvas
        self.drawn  = None
        self.layer = layer
        
    def onStart(self, event):
        self.start = event
        self.drawn = None

    # dynamicly draw the circle
    def onGrow(self, event):                          
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = canvas.create_oval(self.start.x, self.start.y, event.x, event.y, outline=self.layer.color, width='2')
        if trace: print objectId
        self.drawn = objectId

    def onMove(self, event):
        if self.drawn:            
            if trace: print self.drawn
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event

# class for zoom to extent
class Zoom2ExtentEvent: 
    def __init__(self, can, map):
        can.bind('<ButtonPress-1>', self.onStart)  
        can.bind('<B1-Motion>',     self.onGrow)   
        can.bind('<ButtonRelease-1>', self.onRelease)   
        self.canvas = can
        self.drawn  = None
        self.map = map
        
    def onStart(self, event):
        self.start = event
        self.drawn = None

    # dynamicly draw the extent box
    def onGrow(self, event):                          
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y, width='2')
        if trace: print objectId
        self.drawn = objectId

    def onRelease(self, event):
        self.canvas.delete(self.drawn)
        self.canvas.delete('all')
        if self.start.x == event.x:
            return
        # the window coordinates of the center of the extent
        cWinX = (self.start.x + event.x)/2
        cWinY = (self.start.y + event.y)/2
        
        # the map cooridnates of the center of the extent
        self.map.center.x = transform2X(cWinX, self.map)
        self.map.center.y = transform2Y(cWinY, self.map)
        
        # ratio to compare the extent to the window
        ratioX = 800/abs(self.start.x - event.x)
        ratioY = 600/abs(self.start.y - event.y)

        ratio = max(ratioX, ratioY)
        self.map.ratio*=ratio
        self.map.vis()
