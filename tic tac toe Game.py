class Board():
    def __init__(self):
        self.cells=[" "," "," "," "," "," "," "," "," "," "," "]

    def display(self):
        print("WELCOME TO TIC - TAC - TOE GAME\n")
        print("%s | %s | %s" %(self.cells[1], self.cells[2], self.cells[3]))
        print("----------")
        print("%s | %s | %s" %(self.cells[4], self.cells[5], self.cells[6]))
        print("----------")
        print("%s | %s | %s" %(self.cells[7], self.cells[8], self.cells[9]))

    def update_cell(self,cell_no, player):
        if self.cells[cell_no] == " ":
            self.cells[cell_no] = player   #updated values
            
    def winner(self, player):   #to check winning conditions
        if self.cells[1]==player and self.cells[2]==player and self.cells[3]==player:
            return True
        if self.cells[4]==player and self.cells[5]==player and self.cells[6]==player:
            return True
        if self.cells[7]==player and self.cells[8]==player and self.cells[9]==player:
            return True
        if self.cells[1]==player and self.cells[4]==player and self.cells[7]==player:
            return True
        if self.cells[2]==player and self.cells[5]==player and self.cells[8]==player:
            return True
        if self.cells[3]==player and self.cells[6]==player and self.cells[9]==player:
            return True
        if self.cells[1]==player and self.cells[5]==player and self.cells[9]==player:
            return True
        if self.cells[3]==player and self.cells[5]==player and self.cells[7]==player:
            return True
        return False
    
    def is_tie(self):   #to check tie after a win
        used_cells = 0
        for cell in self.cells:
            if cell != " ":
                used_cells+=1

        if used_cells == 9:
            return True
        else:
            return False
        
    def reset(self):   #to display an empty board
        self.cells=[" "," "," "," "," "," "," "," "," "," "," "]
board=Board()

def refresh_screen():  #show's the board
    board.display()
refresh_screen()

while True:
    x_choice=int(input("\nX> CHOOSE FROM 1 TO 9: "))   #get x input
    board.update_cell(x_choice, "X")   #update X's value

    refresh_screen()
    if board.winner("X"):   #if X wins ---
        print("\nX WINS!\n")
        play_again=input("Would you like to play again? (Y/N): ").upper()   #another try
        if play_again == "Y":
            board.reset()
            continue
        else:
            break

    if board.is_tie():   #returns a tie
        print("\nTIE GAME\n")
        play_again=input("Would you like to play again? (Y/N): ").upper()   #another try
        if play_again == "Y":
            board.reset()
            continue
        else:
            break
        
    o_choice=int(input("\nO> CHOOSE FROM 1 TO 9: "))   #get o input
    board.update_cell(o_choice, "O")   #update O's value
    
    refresh_screen()
    if board.winner("O"):   #if O wins ---
        print("\nO WINS!\n")
        play_again=input("Would you like to play again? (Y/N): ").upper()   #another try
        if play_again == "Y":
            board.reset()
            continue
        else:
            break

    if board.is_tie():   #returns a tie
        print("\nTIE GAME\n")
        play_again=input("Would you like to play again? (Y/N): ").upper()   #another try
        if play_again == "Y":
            board.reset()
            continue
        else:
            break
