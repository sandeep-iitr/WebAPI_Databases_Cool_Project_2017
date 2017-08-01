# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:51:42 2017

@author: Brent Usui
"""
L= []
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], ['X', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],['X', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
for i, row in enumerate(board):
    L.append(board[i][0])
    

print ("".join(L))