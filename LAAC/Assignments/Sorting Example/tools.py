from graphics import *
import re
import math

class sortVisualizer(object):
    def __init__(self):
        self.name = ''
        self.data = []
        self.points = []
        self.win = GraphWin("Sort example", 500, 500)
    def updateData(self, newData):
        if len(newData) != 0:
            # create a shallow copy of newData
            if len(self.data) == 0:
                ind = 0
                # draw the balls
                for s in newData:
                    p = Circle(Point(s*2, ind*2), 2)
                    p.draw(self.win)
                    self.points.append(p)
                    ind = ind + 1
            else:
                # update the graphics
                ind = 0
                for p in self.points:
                    dx = 2*self.data[ind]-(p.getCenter()).getX()
                    y = (p.getCenter()).getY()
                    ind = ind + 1
                    p.move(dx, 0)

        self.data = newData[:]

class location(object):
    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.neighbors = []
  
