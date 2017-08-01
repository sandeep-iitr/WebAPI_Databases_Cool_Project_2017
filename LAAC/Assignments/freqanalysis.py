# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:34:18 2017

@author: Brent Usui
"""

def func():
    url = input()
    url = url.lower()
    
    key = 'abcdefghijklmnopqrstuvwxyz1234567890'
    
    myList = []
    
    for char in key:
        myList.append(0)
    
    for char in url:
        if(key.find(char) != -1):
            myList[key.find(char)] = myList[key.find(char)] + 1
        
        
   
    char = key[0]
    while(len(key) > 0): 
        pos = -1
        myMax= -1
        for ind, check in enumerate(key):
            if(myList[ind] > myMax):
                myMax = myList[ind]
                pos = ind
        
        print (key[pos], myMax, "%0.4f" % (myMax/len(url)))
        key = key[:pos] + key[pos+1:]
        del myList[pos]
        
        
        
        
        
