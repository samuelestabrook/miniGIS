from Tkinter import *
from tkMessageBox import *
from Map import *
import tkMessageBox, tkFileDialog
from Commons import *

def notdone():  
    showerror('Not implemented', 'Not yet available')
    
def exitGIS():
    if tkMessageBox.askokcancel("Exit", "Wanna leave?"):
        root.destroy()

def importShp():
    dirname = tkFileDialog.askdirectory(parent=root,initialdir=".",title='Please select a directory') 
    map.openMap(dirname)

def addShp():
    shpFile = tkFileDialog.askopenfilename(parent=root,initialdir=".",title='Please select a shpfile',
                                           defaultextension='.shp', filetypes=(("shp file", "*.shp"),("all files", "*.*")))
    layer = map.addLayer(os.path.splitext(shpFile)[0], randomColor())
    if len(map.layers) == 1:
        map.initVisParameter()
    # delete all, then redraw to make sure the layer visualization order polygon->polylin->point
    can.delete('all')
    map.vis()
    
def close():
    if tkMessageBox.askokcancel("Exit", "Wanna close?"):
        can.delete('all')
    map.clean()
    
# need to unbind all the button events in the canvas before operations
# other operations are same
def zoomIn2Times():
    can.delete('all')
    map.zoomIn2Times()

def zoomOut2Times():
    can.delete('all')
    map.zoomOut2Times()

def zoom2Full():
    can.delete('all')
    map.zoom2Full()

def zoom2Extent():
    unbindCanvas(can)
    map.zoom2Extent()
    
def addPoint():
    unbindCanvas(can)
    map.addPoint()               

def addPolyline():
    unbindCanvas(can)
    map.addPolyline()

def addCircle():
    unbindCanvas(can)
    map.addCircle()
    
def addPolygon():
    unbindCanvas(can)
    map.addPolygon()
    
def closeLayer():
    map.closeLayer()
    

def checkIntersect():
    map.checkIntersect()
    
def makemenu(win):
    top = Menu(win)       
    win.config(menu=top)
    
    file = Menu(top, tearoff=0)
    file.add_command(label='Import Shp',  command=importShp,  underline=0)
    file.add_command(label='Add Shp Layer',  command=addShp,  underline=0)
    file.add_command(label='Close', command=close,  underline=0)
    file.add_command(label='Exit',    command=exitGIS, underline=0)
    top.add_cascade(label='File',     menu=file,        underline=0)

    view = Menu(top, tearoff=0)
    view.add_command(label='Zoom In',     command=zoomIn2Times,  underline=0)
    view.add_command(label='Zoom Out',   command=zoomOut2Times,  underline=0)
    view.add_command(label='Zoom Full',   command=zoom2Full,  underline=0)
    view.add_command(label='Zoom Extent',   command=zoom2Extent,  underline=0)
    view.add_command(label='Close Layer',   command=closeLayer,  underline=0)
    top.add_cascade(label='View',     menu=view,        underline=0)

    edit = Menu(top, tearoff=0)
    edit.add_command(label='Draw Point',     command=addPoint,  underline=0)
    edit.add_command(label='Draw Polyline',   command=addPolyline,  underline=0)
    edit.add_command(label='Draw Circle',   command=addCircle,  underline=0)
    edit.add_command(label='Draw Polygon',   command=addPolygon,  underline=0)
    top.add_cascade(label='Edit',     menu=edit,        underline=0)

    intersect = Menu(top, tearoff=0)
    intersect.add_command(label='Check Intersect',     command=checkIntersect,  underline=0)
    top.add_cascade(label='Intersect',     menu=intersect,        underline=0)
    

if __name__ == '__main__':
    global root
    global can
    global map

    root = Tk()         
    root.title('MiniGIS')
    can = Canvas(root, width = 800, height = 600)
    map = Map(can, 800, 600)
    can.pack()
    makemenu(root)        

    root.mainloop()
