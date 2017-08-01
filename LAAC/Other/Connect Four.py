# initiating some variables
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
spot = [0, 0, 0, 0, 0, 0, 0]
row = 0;
col = 0;



# function to display the board
def displayBoard():
    print("   =====CONNECT FOUR=====")
    
    # draws the line across the top
    string = ""
    for i in range(0, 9):
        string = string + "---"
        
    string = string + "--"   
    print(string)
    
    
    
    # draws the rest of the board
    for indRow, row in enumerate(board):
        string = ""
        
        # draws the line with the chips
        for indCol, col in enumerate(board[indRow]):
            string = string + "| " + str(board[indRow][indCol]) + " "
        string = string + "|"
            
        print(string)
        
        
        # draws the extra lines across the board
        string = ""
        for i in range(0, 9):
            string = string + "---"
            
        string = string + "--"   
        print(string)
        
    print ("  1   2   3   4   5   6   7")      
    
#========================= End of displayBoard() ==============================



# function to check if the last move wins the game
# input row and col index of the last move
def checkWin(row, col, player):
# checking the board horizontally
 
    L = board[row]
    L = "".join(L)
    
    if(L.find(player*4) >= 0):
        return True
    
# checking the board vertically
    L = ""
    for ind, indRow in enumerate(board):
        L = L + board[ind][col]
        
    if(L.find(player*4) >= 0):
        return True


# checking the board diagonally (forward slash)
    count = 1
    L = board[row][col]
    while(row-count >= 0 and col+count < 7):
        L = L + board[row-count][col+count]
        count = count + 1
    
    count = 1    
    while(row+count < 6 and col-count >= 0):
        L = board[row+count][col-count] + L
        count = count + 1
    
    
    if(L.find(player*4) >= 0):
        return True    
    
    
# checking the board diagonally (back slash)    
    count = 1
    L = board[row][col]
    while(row+count < 6 and col+count < 7):
        L = L + board[row+count][col+count]
        count = count + 1
    
    count = 1
    while(row-count >= 0 and col-count >= 0):
        L = board[row-count][col-count] + L
        count = count + 1
        

    if(L.find(player*4) >= 0):
        return True
    
    
# if there is no win then return False
    
    return False    

#========================= End of checkWin() =================================



# function that asks one of the two players to put in a valid answer
def prompt(turn):
    answer = ""
    
# Checks if the input from the user is valid
    goodAnswer = False
    while(goodAnswer == False):
        print("Where will you put your chip? (1-7)")
        answer = input();
        
        if(answer.isdigit()):
            answer = int(answer) - 1
            if(answer >= 0 and answer < 7):
                if(spot[answer] < 6):
                    spot[answer] = spot[answer] + 1
                    goodAnswer = True
                
                else:
                    displayBoard()
                    print('\nInvalid Input')
            
            else:
                displayBoard()
                print('\nInvalid Input')
            
        
        else:
            displayBoard()
            print('\nInvalid Input')
    

# assigning the location of the chip to row and col
    global col
    global row
    col = answer
    row = 6-spot[answer]   


# placing the chip on the board
    if(turn == 0):
        board[row][col] = 'O'
    
    else:
        board[row][col] = 'X'    
    
    
    
#========================= End of prompt()====================================
    


# main program which runs the game
count = 0  
turn = 0   #   0 -> O      1 -> X
noWin = True


# stops game if someone wins or the board is filled
while(noWin and count < 42):
    displayBoard();
    prompt(turn)
    
    
# O's turn    checks if the last play won
    if(turn == 0):
        if(checkWin(row, col, 'O')):
            displayBoard()
            print("Player O wins!!!")
            noWin= False
        
        else:
            turn = 1
    
    
# X's turn    checks if the last play won
    elif(turn == 1):
        if(checkWin(row, col, 'X')):
            displayBoard()
            print("Player X wins!!!")
            noWin = False
            
        else:
            turn = 0;


# counts for the amount of chips on the board
    count = count + 1
    
if(noWin):
    displayBoard()
    print("It's a tie.")

