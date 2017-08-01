#!/usr/bin/env python

from graphics import *
import re
import math
import random
import time

def main():
  
    N = input("Enter N: ")
    print ("N= %s"%N)
    M = int(N)
    numbers = list(range(0, M+1))
    
    # randomly shuffle the numbers
    random.shuffle(numbers)
    numbersCopy=list(numbers)
    #sv.updateData(numbers)
    print ("Python sort uses the TimSort algorithm https://en.wikipedia.org/wiki/Timsort")
    pythonSortStartTime=time.time();
    numbersCopy.sort()
    print("--- %s seconds ---" % (time.time() - pythonSortStartTime))
    print("Python sort is done!\n")
    bubbleStartTime=time.time();
    numbersBubble = mySort(numbers)
    print("--- %s seconds ---" % (time.time() - bubbleStartTime))
    print("Bubble sort is done!\n")
    cmpRes=cmp(numbers,numbersCopy)
    if cmpRes == 0:
        print ("After sorting both lists are identical")
    else:
        print ("The two sorted lists are DIFFERENT!!")
        
def mySort(numbers):
    bubbleSort (numbers)
    return numbers



def bubbleSort(List):
    #write bubble sort code here
    return List

def cmp(a, b):
    return (a > b) - (a < b) 

        
if __name__ == "__main__":
	import sys
	import re
	from graphics import *
	from tools import *
main()
    
