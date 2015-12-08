from Layer import *
from Tkinter import *
import glob, os
from Dialogs import *
from Commons import *
from Events import *

import tkMessageBox

class Map:
    # init map
    # can is the canvas
    # winWidth is the window width
    # winHeight is the window height
    def __init__(self, can, winWidth, winHeight):     
        self.windowWidth, self.windowHeight = winWidth, winHeight
        self.can = can
        self.layers = []
        self.bbxset = False # bounding box
        
        self.zoomFactor = 1
        self.ratio=1
        self.mode = ProjMode.CENTER
        
        # This is used to save the intersect points between two polyline layers
        self.intersects = []

    # open the shape files in the directory
    def openMap(self, mapDir):
        try:
            if None == mapDir:
                return
            os.chdir(mapDir)
            print mapDir
            files = glob.glob(os.path.join(mapDir, '*.shp'))
            if None == files or 0 == len(files):
                tkMessageBox.showinfo("Select directory", "Please select a directory which contains shape files")
                return
            for file in files:
                file = os.path.splitext(file)[0]
                self.addLayer(file, randomColor())
                print file
            self.initVisParameter()
            self.vis()
        except WindowsError:
            print  tkMessageBox.showinfo("Select directory", "Please select a directory which contains shape files")

    
    def zoomIn2Times(self):
        self.zoomFactor = 0.5
        self.calculate()
        self.vis()
        
    def zoomOut2Times(self):
        self.zoomFactor = 2.0
        self.calculate()
        self.vis()

    # zoom to full screen
    def zoom2Full(self):
        
        self.zoomFactor = 1
        self.initVisParameter()
        self.vis()

    # zoom to extent
    def zoom2Extent(self):
        Zoom2ExtentEvent(self.can,self)

    # initilize the visualization paramerter
    def initVisParameter(self):
        ratiox = self.windowWidth/(self.maxx-self.minx)
        ratioy = self.windowHeight/(self.maxy-self.miny)
        self.ratio = min(ratiox,ratioy)
        self.setCenterFromBBox([self.minx, self.miny, self.maxx, self.maxy])
        
    def setCenterFromBBox(self, bBox):
        self.center = Point((bBox[0] + bBox[2])/2, (bBox[1] + bBox[3])/2)

    #determines ratio, pick smaller one; do it each time a new layer is added   
    def calculate(self):        
        self.ratio /= self.zoomFactor
        
    #creates layer with file name, appends to layers list   
    def addLayer(self, fileName,color):
        layer = Layer(fileName, color)
        if layer != 0:
            self.layers.append(layer)
            if self.bbxset: #bounding box for map is reset each time a layer is added
                if self.minx > layer.minx:
                    self.minx = layer.minx
                if self.miny > layer.miny:
                    self.miny = layer.miny
                if self.maxx < layer.maxx:
                    self.maxx = layer.maxx
                if self.maxy < layer.maxy:
                    self.maxy = layer.maxy
            else:
                self.minx = layer.minx
                self.miny = layer.miny
                self.maxx = layer.maxx
                self.maxy = layer.maxy
                self.bbxset = True
        return layer

        
    # draw Point using mouse
    def addPoint(self):
        d = LayerDialog(self.can, self.layers)
        self.can.wait_window(d.top)  
        selectedLayer = d.get()
        if selectedLayer == None or selectedLayer.shapeType != 1:
            tkMessageBox.showinfo("Select layer", "Please select point layer to draw point")
            return
        dc = PointDraw(self.can, selectedLayer)

    # draw Circle using mouse
    def addCircle(self):
        d = LayerDialog(self.can, self.layers)
        self.can.wait_window(d.top)  
        selectedLayer = d.get()
        if selectedLayer == None or selectedLayer.shapeType != 3:
            tkMessageBox.showinfo("Select layer", "Please select polyline layer to draw circle")
            return
        dc = CircleDraw(self.can, selectedLayer)

    # draw polyline using mouse
    def addPolyline(self):
        d = LayerDialog(self.can, self.layers)
        self.can.wait_window(d.top)  
        selectedLayer = d.get()
        if selectedLayer == None or selectedLayer.shapeType != 3:
            tkMessageBox.showinfo("Select layer", "Please select polyline layer to draw circle")
            return
        dc = PolylineDraw(self.can, selectedLayer)

    # draw polygon using mouse
    def addPolygon(self):
        d = LayerDialog(self.can, self.layers)
        self.can.wait_window(d.top)  
        selectedLayer = d.get()
        if selectedLayer == None or selectedLayer.shapeType != 5:
            tkMessageBox.showinfo("Select layer", "Please select polygon layer to draw polygon")
            return
        dc = PolygonDraw(self.can, selectedLayer)

    # close(delete) a layer from the map
    def closeLayer(self):
        d = LayerDialog(self.can, self.layers)
        self.can.wait_window(d.top)  
        layerIndex = d.get()
        if not d.ok:
            return
        try:
            self.layers.remove(layerIndex)
            self.can.delete('all')
            self.vis()
        except IndexError:
            print "Oops, layer index error"

    # check intersections between two different polyline layers
    def checkIntersect(self):
        d = PolylineLayerDialog(self.can, self.layers)
        self.can.wait_window(d.top)
        if not d.ok:
            return
        selectedPolylineLayers = d.get()
        if len(d.get())!=2:
            tkMessageBox.showinfo("Select layers", "Please select two polyline layers")
            return
        
        self.intersects = selectedPolylineLayers[0].checkIntersects(selectedPolylineLayers[1])

        self.visIntersects()

    # visualize the map in the canvas
    def vis(self):
        print 'map ratio is:', self.ratio
        #Need to visualize the layers by order
        for layer in self.layers:
            if(layer.shapeType == 5):
                layer.vis(self)
        for layer in self.layers:
            if(layer.shapeType == 3):
                layer.vis(self)
        for layer in self.layers:
            if(layer.shapeType == 1):
                layer.vis(self)
        for point in self.intersects:
            point.vis(self, layer.color)
        
        self.visIntersects()
        self.can.pack()

    # visulize the intersections
    def visIntersects(self):
        for point in self.intersects:
            point.visInterseccts(self)

    def clean(self):
        self.layers = []
        self.bbxset = False # bounding wasn't set up yet 
        
        self.zoomFactor = 1
        self.ratio=1
        self.mode = ProjMode.CENTER
        
        # This is used to save the intersect points between two polyline layers
        self.intersects = []
