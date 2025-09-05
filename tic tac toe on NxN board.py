class Board:
    def __init__(self, size):
        self.size = size
        self.total_cells = size * size
        self.cells = [" "] * self.total_cells

    def display(self):
        print("\nWELCOME TO TIC - TAC - TOE GAME ({}x{})\n".format(self.size, self.size))
        for i in range(self.size):
            row = [self.cells[i * self.size + j] for j in range(self.size)]
            print(" | ".join(row))
            if i < self.size - 1:
                print("-" * (self.size * 4 - 3))  # dynamic separator

    def update_cell(self, cell_no, player):
        index = cell_no - 1
        if 0 <= index < self.total_cells and self.cells[index] == " ":
            self.cells[index] = player
            return True
        else:
            print("Cell already taken or invalid! Try again.")
            return False

    def winner(self, player):
        N = self.size
        
        for i in range(N):   #chech rows
            if all(self.cells[i * N + j] == player for j in range(N)):
                return True
        
        for j in range(N):   #check columns
            if all(self.cells[i * N + j] == player for i in range(N)):
                return True
        
        if all(self.cells[i * N + i] == player for i in range(N)):   #chack main diagonal
            return True
        
        if all(self.cells[i * N + (N - 1 - i)] == player for i in range(N)):   #check anti-diagonal
            return True
        return False

    def is_tie(self):
        return all(cell != " " for cell in self.cells)

    def reset(self):
        self.cells = [" "] * self.total_cells


def play_game():
    size = int(input("Enter board size (N for NxN): "))
    board = Board(size)

    current_player = "X"
    while True:
        board.display()
        try:
            move = int(input(f"\n{current_player}> Choose a cell (1-{board.total_cells}): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if not board.update_cell(move, current_player):
            continue

        if board.winner(current_player):
            board.display()
            print(f"\n{current_player} WINS!\n")
            play_again = input("Would you like to play again? (Y/N): ").upper()
            if play_again == "Y":
                board.reset()
                current_player = "X"
                continue
            else:
                break

        if board.is_tie():
            board.display()
            print("\nTIE GAME\n")
            play_again = input("Would you like to play again? (Y/N): ").upper()
            if play_again == "Y":
                board.reset()
                current_player = "X"
                continue
            else:
                break

        current_player = "O" if current_player == "X" else "X"   #to switch player

play_game()
