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
  
class world(object):
    def __init__(self):
        self.name = ''
        self.height = 0
        self.width = 0
        self.locations = {}

    def create_map(self, fname):
        pic = Image(Point(0, 0), fname)
        self.width = pic.getWidth();
        self.height = pic.getHeight();

        win = GraphWin("Map", self.width, self.height)

        pic2 = Image(Point(self.width/2, self.height/2), fname)
        pic2.draw(win)
        self.win = win
        
    def read_locations(self, fname):
        f = open(fname, 'r')
        print ("Opening location file",fname)
        line = f.readline()
        while line:
            cmdlist = re.findall(r'[\S]+', line)
            if len(cmdlist) > 0:
                newLocation = location();
                newLocation.name = cmdlist[0]
                newLocation.x = float(cmdlist[1])
                newLocation.y = float(cmdlist[2])
                self.locations[cmdlist[0]] = newLocation
                #print "Read location %s" % newLocation.name
            line = f.readline()
        f.close()

    def draw_locations(self):
        # use markers that are 1/20th of the width and heigth
        dx = self.width/200
        dy = self.height/200
        
        for currentLocation in self.locations.values():
            c = Circle(Point(currentLocation.x, currentLocation.y), dx)
            c.setFill('red')
            c.draw(self.win)
            
            t = Text(Point(currentLocation.x, currentLocation.y), currentLocation.name)
            t.draw(self.win)

    def get_locations(self):
        r = Rectangle(Point(self.width-100,self.height-50), Point(self.width, self.height))
        r.setFill(color_rgb(200, 200, 200))
        r.draw(self.win)
        t = Text(Point(self.width-50, self.height-25), "Finish")
        t.draw(self.win)
        entry = False
        while 1:

            p = self.win.getMouse()
                
            if (p.getX() >self.width-100) & (p.getY() > self.width-50):
                break
            else:
                print ((p.getX(), p.getY()))
                
    def find_locations(self):
        r = Rectangle(Point(0,0), Point(200, 100))
        r.setFill(color_rgb(200, 200, 200))
        r.draw(self.win)
        t = Text(Point(100, 50), "Finish")
        t.draw(self.win)
        entry = False
        while 1:
 

            p = self.win.getMouse()
            if entry:
                nl = location()
                nl.name = e.getText()
                nl.x = pold.getX()
                nl.y = pold.getY()
                self.locations[nl.name] = nl
                
            if (p.getX() < 200) & (p.getY() < 100):
                break
            else:
                entry = True
            e = Entry(p, 20)
            e.draw(self.win)
            pold = p
            
    def write_locations(self, fname):
        f = open(fname, 'w')
        for currentLocation in self.locations.values():
            f.write("%s %d %d\n" % (currentLocation.name, currentLocation.x, currentLocation.y))
        f.write("\n\n")
        f.close()

    def input_trip(self, clist):
        ind = 0
        distT = 0
        for cloc in clist:
            c = Circle(Point(cloc.x, cloc.y), 5)
            c.setFill('yellow')
            c.draw(self.win)
            t = Text(Point(cloc.x, cloc.y), cloc.name)
            t.draw(self.win)
            if ind == 0:
                pic = Image(Point(cloc.x, cloc.y), 'pic.gif')
                pic.draw(self.win)
            if ind > 0:
                l = Line(Point(cloc.x, cloc.y), Point(oloc.x, oloc.y))
                l.draw(self.win)
                
                dist = get_distance(cloc, oloc)
                distT = distT + dist
                N = int(round(dist/50, 0))
                dx = (cloc.x-oloc.x)/N
                dy = (cloc.y-oloc.y)/N
                for i in range(1, N+1):
                    pic.move(dx, dy)
                #pic.draw(self.win)
            oloc = cloc
            ind = ind + 1
        print ("Total distance: %f miles", distT)

def get_distance_xy(x1, y1, x2, y2):
    return 500*math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))/150

def get_distance(loc1, loc2):
    return get_distance_xy(loc1.x, loc1.y, loc2.x, loc2.y)
