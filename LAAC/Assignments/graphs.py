#!/usr/bin/python2.6
 
# Graph Theory easy exercises for Social Networks module
# LACC 2016
 
#*************************************
# This is where you write your code
#
# matrix_load()
#
# Loads an adjacency matrix for a graph from a file
#
# input: none
# output: matrix containing each node 
# 
# Note: You can open a file using open("filename.txt")
# 
# You can get a list containing each line with file.readlines()
#
# You'll need to grab each number from each line, cast it to an
# int using int() and place it into your matrix
#
# A matrix is just a double list (e.g., x[][] )
#*************************************

N= 0
def matrix_load():
    file = open("matrix.txt")

    matrix = []


    string = file.readlines()

    global N
    N = int(string[0])

    for i in range(1, N+1):
        dummy = []
        for j in range(0, N):
            dummy.append(string[i][j])
        
        matrix.append(dummy)
    
    file.close()
    return matrix
#*************************************
# This is where you write your code
#
# print_degrees(mat)
#
# Prints the degrees of all nodes in a graph given an adj. matrix 
#
# input: the adjacency matrix of the graph
# output: none
# 
# Note: You don't need to return anything. 
#
# Effectively, you'll need to count the number of 1s in each row 
# (or each column) and print this. Use a nested loop (for or while)
#*************************************
 
def print_degrees():
    
    
    matrix = matrix_load()
    
    total = []
    
    for i in range(0, N):
        count = 0
        for j in range(0, N):
            if(int(matrix[i][j]) == 1):
                count = count + 1
            
        
        total.append(count)
    
    
    for i in range(0, N):
        print((i+1), total[i])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    