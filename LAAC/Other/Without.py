board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
spot = [0, 0, 0, 0, 0, 0, 0]
row = 0;
col = 0;


def displayBoard():
    print("   =====CONNECT FOUR=====")
    
    string = ""
    for i in range(0, 9):
        string = string + "---"
        
    string = string + "--"   
    print(string)
    
    
    for indRow, row in enumerate(board):
        string = ""
        
      
        for indCol, col in enumerate(board[indRow]):
            string = string + "| " + str(board[indRow][indCol]) + " "
        string = string + "|"
            
        print(string)
        
        string = ""
        for i in range(0, 9):
            string = string + "---"
            
        string = string + "--"   
        print(string)
        
    print ("  1   2   3   4   5   6   7")      
    
    
def checkWin(row, col, player):
 
    L = board[row]
    L = "".join(L)
    
    if(L.find(player*4) >= 0):
        return True
    
    
    L = ""
    for ind, indRow in enumerate(board):
        L = L + board[ind][col]
        
    if(L.find(player*4) >= 0):
        return True

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
    
    return False    


def prompt(turn):
    answer = ""
    
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
    
    global col
    global row
    col = answer
    row = 6-spot[answer]   

    if(turn == 0):
        board[row][col] = 'O'
    
    else:
        board[row][col] = 'X'    
    
    
count = 0  
turn = 0   
noWin = True


while(noWin and count < 42):
    displayBoard();
    prompt(turn)
    
    
    if(turn == 0):
        if(checkWin(row, col, 'O')):
            displayBoard()
            print("Player O wins!!!")
            noWin= False
        
        else:
            turn = 1
        
    elif(turn == 1):
        if(checkWin(row, col, 'X')):
            displayBoard()
            print("Player X wins!!!")
            noWin = False
            
        else:
            turn = 0;

    count = count + 1
    
if(noWin):
    print("It's a tie.")

