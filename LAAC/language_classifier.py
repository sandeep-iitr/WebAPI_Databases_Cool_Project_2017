#!/usr/bin/python2.6

# Language classifier miniproject for machine learning module
# LACC 2016

#*************************************
# This is where you write your code
#
# train(training_set)
#
# Loads a language training set from a text file
#
# input: name of the training set (for example, "french.txt")
# output: dictionary containing word/frequency pairs 
# 
# Note: You can open a file using open("filename.txt")
# 
# You can get a list containing each line with file.readlines()
#
# You'll need to grab each word from each line, and add 1 to the 
# frequency of that word in your dictionary. Try to strip out symbols.
#
# You can learn more about Python dictionaries online: http://www.tutorialspoint.com/python/python_dictionary.htm
#*************************************
import math



def train(training_set):
    myString = open(training_set)
    myString = myString.readlines()
    myDict = {}
    
    for i in range(0, len(myString)):
        if(i == "\n" or i == ""):
            continue
        
        myString[i] = myString[i].lower()
        myString[i] = myString[i].replace('.', "")
        myString[i] = myString[i].replace(',', "")
        myString[i] = myString[i].replace("'", "")
        myString[i] = myString[i].replace('"', "")
        myString[i] = myString[i].replace('-', "")
        myString[i] = myString[i].replace('?', "")
        myString[i] = myString[i].replace('!', "")
        myString[i] = myString[i].replace(':', "")
        myString[i] = myString[i].replace(';', "")
        myString[i] = myString[i][0:len(myString[i])-2]
        
    
    for i in range(0, len(myString)):    
        dummy = myString[i].split(" ")
        
        for j in dummy:
            try:
                myDict[j] = myDict[j] + 1
 
            except KeyError:
                myDict[j] = 1
            
    
    return myDict    




#*************************************
# This is where you write your code
#
# classify(language1, language2, phrase)
#
# Classifies a phrase as being from language1 or language2 
#
# input: the language dictionaries for language1 and language2 
# and the phrase to be classified
# output: 0/1 for which of the two languages 
# 
# You should use a naive Bayes classifier. Break up the phrase 
# to be classified into separate words, and compute the probability
# of each word to be from the French language (with the help of the 
# dictionaries). Use the formula:
# P(word|French) = (# of copies of word in French training set + 1) 
#					/ (# of words in training set + 1)
# The overall probability of the phrase is the product of all the 
# word probabilities (because of the naive independence assumption)
#
# Compute a probability for French and one for Spanish
# The larger is the one we classify to
#*************************************

def classify(language1, language2, language3, phrase):
    List = ["french", "spanish", "german"]
    
    languages = []
    languages.append(train(language1))
    languages.append(train(language2))
    languages.append(train(language3))
                              
    
    phrase = phrase.lower()
    phrase = phrase.replace(".", "")
    phrase = phrase.replace(",", "")
    phrase = phrase.replace("'", "")
    phrase = phrase.replace('"', "")
    phrase = phrase.replace("?", "")
    phrase = phrase.replace("!", "")
    phrase = phrase.replace("-", "")
    phrase = phrase.replace(":", "")
    phrase = phrase.replace(";", "")
    myList = phrase.split(" ")


    probList = []
    for i in range(0, len(languages)):
        probList.append(0)
        for j in myList:
            try:
                prob = math.log10((languages[i][j]+1) / (len(languages[i])+1))
                probList[i] = probList[i] + prob
            
            except:
                prob = math.log10(1 / (len(languages[i])+1))
                probList[i] = probList[i] + prob
            
    

            
    
    myMax = -1000000000000
    ind = -1
    for i, num in enumerate(probList):
        print(List[i], num)
        if(myMax < num):
            ind = i
            myMax = num
    
    
    print(List[ind])
        



phrase = "Der Drachen besteht darauf, dass wir ihm eine Jungfrau als Opfer bringen, anderenfalls wird er das Dorf völlig niederbrennen"
classify("french.txt", "spanish.txt", "german.txt", phrase)
    








  
