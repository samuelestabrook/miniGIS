import random

#projection mode
class ProjMode:
    CENTER = 1
    LEFTTOP = 2

#random create color
def randomColor():
    r = lambda: random.randint(0,255)
    return ('#%02X%02X%02X' % (r(),r(),r()))

#check if two bbox don't overlay
#if they dont overlay, bbox1 is outside of bbox2, return true
def checkIsOutside(bbox1, bbox2):
    return bbox1[0] > bbox2[2] or bbox1[1] > bbox2[3] or bbox1[2] < bbox2[0] or bbox1[3] < bbox2[1]

#project map coordinate to screen coordinate in different mode
def transformX(x, map):
    if map.mode == ProjMode.CENTER:
        return (x - map.center.x)*map.ratio + 400
    elif map.mode == ProjMode.LEFTTOP :
        return int((x-map.minx)*map.ratio)
    else:
        return None

def transformY(y, map):
    if map.mode == ProjMode.CENTER:
        return (map.center.y - y)*map.ratio + 300
    elif map.mode == ProjMode.LEFTTOP:
        return int((map.maxy-y)*map.ratio)
    else:
        return None

#project screen coordinates to map corrdications
def transform2X(winx, map):
    if map.mode == ProjMode.CENTER:
        return (winx - 400)/map.ratio + map.center.x
    elif map.mode == ProjMode.LEFTTOP :
        return winx/map.ratio + map.minx
    else:
        return None

def transform2Y(winy, map):
    if map.mode == ProjMode.CENTER:
        return map.center.y - (winy -300)/map.ratio
    elif map.mode == ProjMode.LEFTTOP:
        return map.maxy-winy/map.ratio
    else:
        return None

def unbindCanvas(can):
    can.unbind('<ButtonPress-1>')
    can.unbind('<B1-Motion>')
    can.unbind('<ButtonRelease-1>')
    can.unbind('<Button-1>')
    can.unbind('<Button-3>')
