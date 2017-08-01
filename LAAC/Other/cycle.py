# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:02:04 2017

@author: Brent Usui
"""
from random import randint


N = 1000
marked = []
matrix = []
def makeMat():
    
    global matrix
    global marked
    
    matrix = []
    for i in range(0, N):
        dummy = []
        for j in range(0, N):
            num = randint(0, 1000)
            if(num >= 999):
                dummy.append(1)
            
            else:
                dummy.append(0)
        
        matrix.append(dummy)
        marked.append(False)

def func():
    makeMat()
    
    detect_cycle(matrix)
  #  print(matrix)
    


def detect_cycle(mat):
    for i in range(0, N):
        global find
        global ori
        global marked
        global path
        
        path = []
        find = False
        ori = i
        pathMaker(i)
        if(find == False):
            for i in range(0, N):
                marked[i] = False
        
        else:
            print(1)
            break
    
    if(find == False):
        print(0)


def pathMaker(index):
    global marked
    global find
    global path
    path.append(index+1)
    marked[index] = True
    
    if(index != ori and len(path) > 2):
        if(find == False and matrix[index][ori] == 1):
            print(path)
            find = True
    
    for i in range(0, N):
        if(i != index):
            if(marked[i] == False and matrix[index][i] == 1):
                pathMaker(i)
                path.remove(i+1)
    
            
    
        
        
    