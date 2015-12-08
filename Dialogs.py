from Tkinter import *
import Tkinter                                                                          
import tkMessageBox

# dialog to select one layer
class LayerDialog:
        def __init__(self, root, layers):
                self.top = Tkinter.Toplevel(root)
                self.layers = layers
                self.var = IntVar()
                i = 0
                for layer in self.layers:
                        Radiobutton(self.top, text=layer.getFileName(), variable=self.var, value=i).pack(anchor=W)
                        i+=1
                button = Tkinter.Button(self.top, text='Ok', command=self.Ok)
                button.pack()
                self.ok = False
                self.selectLayer = None
        def Ok(self):
                # destroy the diallog and set ok to True if click button ok
                self.top.destroy()
                self.ok = True
        def get(self):                                                                 
                return self.layers[self.var.get()]

# dialog to select two polyline layers
class PolylineLayerDialog:
        def __init__(self, root, layers):
                self.top = Tkinter.Toplevel(root)
                # polyline layers list in the dialog 
                self.polylineLayers = []
                # layers selected 
                self.selectedPolylineLayers = []
                # each checkbutton has a IntVar
                self.vs = []
                for layer in layers:
                        if layer.shapeType == 3:
                                v = IntVar()
                                self.polylineLayers.append(layer)
                                Checkbutton(self.top, text=layer.getFileName(), variable=v).pack(anchor=W)
                                self.vs.append(v)
                button = Tkinter.Button(self.top, text='Ok', command=self.Ok)
                button.pack()

                self.ok = False
        def Ok(self):                                                                  
                self.top.destroy()
                self.ok = True
                for i in range(len(self.vs)):
                        if self.vs[i].get():
                                print self.polylineLayers[i].getFileName()
                                self.selectedPolylineLayers.append(self.polylineLayers[i])
                        
        def get(self):                                                                 
                return self.selectedPolylineLayers
