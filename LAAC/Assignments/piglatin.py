# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:19:10 2017

@author: Brent Usui
"""

string = ""
L = []

def prompt():
    print ("Please enter one word with only letters: ")
    
    
    
    
def check():
    for char in string:
        if(char.isalpha()):
            L.append(char)
            
        
        else:
            print("Error: invalid input")
            return False
        
    return True
    
    
    
def translate():
    letter = L[0]
    del L[0]
    
    L.append(letter)
    L.append("ay")
    
    print("".join(L))
    
    
prompt()
string = input()
while(check() == False):
    prompt()
    string= input()
    L = []

else:
    translate()

    
    
    
    
    
    
    

    
    