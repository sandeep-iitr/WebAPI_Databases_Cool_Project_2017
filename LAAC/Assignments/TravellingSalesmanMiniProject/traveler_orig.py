
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
    places = speedyTrip(places)
    
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
def efficientTrip(places):
    
   
    ind = 0
    visited = []
    visited.append(places[0])
    
    while(len(places) > 0):
        myMin = 10000000
        if(len(places) == 1):
            visited.append(places[0])
            places.remove(places[0])
            
        else:
            for j in range(1, len(places)):
                if (visited[len(visited)-1] == places[j]):
                    continue
                
                if (myMin > get_distance(visited[len(visited)-1], places[j])):
                    myMin = get_distance(visited[len(visited)-1], places[j])
                    ind = j
            visited.append(places[ind])
            places.remove(places[ind])
    
    
#    for i in visited:
#       print(i.name)
    return visited
            
        

def speedyTrip(places):
    # places is a list of locations
    # the first place is places[0]
    # places[0].name : name of the first place
    # places[0].x
    # x_location
    # places[0].y
    # y_location
    # get_distance(places[0], places[1]) returns 
    # the distance between places[0] and places[1]
    
    #these are random code statement that you may or may not want to use.
    cities=[]
    unvisited_cities=list(range(0,50))
    visited_cities=[0]
    print (visited_cities)
    print (unvisited_cities)
    unvisited_cities.remove(0)
    next_city= unvisited_cities[0]
    #while unvisited_cities !=[]:
    #   cities.append(next_city)
    
    visited_cities.append(next_city)
    unvisited_cities.remove(next_city)
    
    print (visited_cities)
    # you can iterate through the places as:
    #N = length(places)
    #for i in range(0,N):
    #   x = 0
    #   ye = get_distance(places[i], places[x])
    #   x = x + 1
    #   print ye

    # ...
    # 
    # or 
    # foreach place in places:
    # ...


    # return the places to be evaluated
    places.append(places[0])
    return places

if __name__ == "__main__":
    import sys
    import re
    from graphics import *
    from tools import *
    main("usa")
    
