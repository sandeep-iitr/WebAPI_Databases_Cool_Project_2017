# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:31:47 2017

@author: Brent Usui
"""

def findMean(L):
    total = sum(L)
    return(total / len(L))

def findMedian(L):
    length = len(L)
    if(length % 2 == 0):
        top = length/2 
        bottom = top-1
        
        return ((L[top] + L[bottom])/2)
    
    else:
        return(L[length//2])
    
    
    
    
def findMode(L):
    numCount = 0
    myMax = 1
    mode = [L[0]]
    first = L[0]

    for i, num in enumerate(L):
        if(first == num):
            numCount = numCount + 1
        else:
            if(numCount == myMax):
                mode.append(num)
                
            elif(numCount > myMax):
                mode = [first]
                myMax = numCount
            
            numCount = 1
            first = num
    
    return (mode)
            










print ("Please enter a list of numbers separated by commas:")

string = input()

L = []
L = string.split(',')
L = [float(num.strip()) for num in L]

        
L.sort()
print ("Mean:", findMean(L))
print ("Median:", findMedian(L))
print ("Mode:", findMode(L))