import random
import re
class Board:
    def __init__(self,dim_size,num_bombs):
        self.dim_size=dim_size
        self.num_bombs=num_bombs
        
        self.board=self.make_board()
        self.values_of_board()
        
        
        self.dug= set(); 
        
    def make_board(self):
        #used to make a board using the dim size and number of bombs
        #Using a list of list because the board is 2-d (rows, colums)
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] #creates an array consiting of 'None's  which represents the board
        
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            location= random.randint(0, self.dim_size**2 - 1) #returns a random integer that a <= N <= b (a and b are the constraints of the board)
            
            row = location // self.dim_size
            col = location % self.dim_size
            
            if board[row][col] == '*': #if bomb is already planted continue to plant a new one
                continue
           
            board[row][col] = '*'
            bombs_planted +=1
            
        return board
    
    def values_of_board(self): #checks to see if the spot on the board contains a bomb or not
        for x in range(self.dim_size):
            for y in range(self.dim_size):
                
                if self.board[x][y] == '*':
                    #if the spot contains a bomb, skip
                    continue
                
                self.board[x][y] = self.neighbour_bombs(x,y)
                    
                    
    def neighbour_bombs(self, row, col):
        #top left: (row-1,col-1)
        #top middle: (row-1, col)
        #top right: (row-1, col +1)
        
        #left: (row,col-1)
        #right: (row, col+1)
        
        #bottom left: (row+1,col-1)
        #bottom mid: (row+1 col)
        #bottom right: (row+1, col +1)
        
        num_neighbouring_bombs= 0;
        
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):# checks above and below to see if there is a bomb
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1): # checks left and right to see if there is a bomb
                if r == row and c == col:#skips the original location
                    continue
                elif self.board[r][c] == '*': 
                    num_neighbouring_bombs+=1
                    
        return num_neighbouring_bombs
    
    def dig(self,row,col):
        
        self.dug.add((row,col)) #Stores where we dug into the dug list
        
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):# checks above and below to see if there is a bomb
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1): # checks left and right to see if there is a bomb
                if (r,c) in self.dug:
                    continue #don't dig if already dug
                
                self.dig(r,c)
                    
        return True  #if initial dig didnt hit bomb, we shouldnt hit here      
    
    
    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
       
def play(dim_size=10,num_bombs=10):   
    board= Board(dim_size,num_bombs)     
    
    safe = True
    
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Enter as row,col: ")) 
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            break #This is when the user hits the bomb

    if safe:
        print("GOOD JOB! YOU WIN!")
    else:
        print("YOU LOSE, LOSER! GET BLOW UP!")
        # reveals the full board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': 
    play()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
