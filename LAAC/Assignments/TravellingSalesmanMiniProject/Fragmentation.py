# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:37:01 2017

@author: Brent Usui
"""

global MAX = 9223372036854775807

class line (object):
    
    def __init__ (self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = (p2.y - p1.y) / (p2.x - p1.x)
        self.b = p1.y - m*p1.x
        
        

class point (object):
    
    def __init__ (self, x, y, closeLine):
        self.x = x
        self.y = y
        self.closeLine = closeLine
        
        tempx = (y - x/closeLine.slope - closeLine.b) / (closeLine.slope - 1/closeLine.slope)
        tempy = closeLine.slope*tempx + closeLine.b
        
        ori = get_distance_xy(tempx, tempy, x, y)
        new = get_distance_xy(x, y, closeLine.p1.x, closeLine.p1.y) + get_distance_xy(x, y, closeLine.p2.x, closeLine.p2.y)
        
        self.add = new-ori



def findLine(lineList, point):
    myMin = MAX
    for i in lineList:
        tempx = (point.y - point.x/i.slope - i.b) / (i.slope - 1/i.slope)
        tempy = i.slope*tempx + i.b
        
        dist = get_distance_xy(tempx, tempy, x, y)
        if(dist < myMin):
            myMin = dist
            
        elif(dist == myMin):
            if(



def main(fname):
    
    # create a world
    m = world()
    fn2 = '%s.gif' % fname
    # load the map
    print ("Loading file", fn2)
    m.create_map(fn2)
    m.read_locations('%s.loc' % (fname))
    
    # locations 
    places = list(m.locations.values())
    
    # rearrange the places to decrease the trip time
    places = fragmentTrip(places)
    
    m.input_trip(places)
    m.win.getMouse()

visited = [False]
went = []
counter = 0
#*************************************
# This is where you write your code
# input: all locations
# output: locations (sorted)
#*************************************
def fragmentTrip(places):
    myLine = []
    
    rand = places[3]
    left = places[0];
    right = places[0];
    for ind, i in enumerate(places):
        if(i == 3):
            continue
        
        else:
            if(left.x > i.x):
                left = i
                    
            elif(right.x < i.x):
                right = i
    
        
    
    myLine.append(line(left, rand))
    myLine.append(line(left,right))
    myLine.append(line(rand, right))
    
    places.remove(right)
    places.remove(left)
    places.remove(rand)
    
    unvisited = []
    for i in places:
            
    
    
   

if __name__ == "__main__":
    import sys
    import re
    from graphics import *
    from tools import *
    main("usa")
    
