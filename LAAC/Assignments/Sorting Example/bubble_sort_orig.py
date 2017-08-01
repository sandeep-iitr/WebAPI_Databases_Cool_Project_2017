#!/usr/bin/env python

from graphics import *
import re
import math
import random


def main():
    global sv
    sv = sortVisualizer()
    N = 100
    numbers = list(range(0, N+1))
    
    # randomly shuffle the numbers
    random.shuffle(numbers)
    sv.updateData(numbers)
    numbers = mySort(numbers)   

    # pause until clicked
    sv.win.getMouse()
    
        
def mySort(numbers):
    bubbleSort (numbers)
    sv.updateData(numbers)
    
    sv.win.getMouse()
    
    return numbers



def bubbleSort(List):
#write your code here
#update the graphics every now and then by calling sv.updateData(List)   \
    for i in List:
        for j in range(0, len(List)-1):
            if(List[j] > List[j+1]):
                dummy = List[j]
                List[j] = List[j+1]
                List[j+1] = dummy
                
                sv.updateData(List)
""" 
   masterList = []
    for x in List:
        b = []
        b.append(x)
        masterList.append(b)

    sort = []
    while(len(masterList) > 1):
        sort = []
        for i in range(0, len(masterList) // 2):
            a = masterList[i*2]
            b = masterList[i*2+1]
            for num in b:
                low = 0
                high = len(a)
                
                while(True):
                    mid = (low + high) // 2
                    
                    if(mid == low or mid == high):
                        a.insert(mid, num)
                        break
                    
                    elif(masterList[i*2][mid] > num):
                        low = mid
                    
                    elif(masterList[i*2][mid] < num):
                        high = mid
                    
                    else:
                        a.insert(mid, num)
                        break
            sort.append[a]
        masterList = sort
                    
    return masterList
"""
        
if __name__ == "__main__":
	import sys
	import re
	from graphics import *
	from tools import *
main()
    
