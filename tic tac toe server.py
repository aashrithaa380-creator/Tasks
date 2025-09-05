import socket
class Board:
    def __init__(self, size):
        self.size = size
        self.total = size * size
        self.cells = [" "] * self.total

    def display(self):
        print("\nCurrent Board:")
        for i in range(self.size):
            row = [self.cells[i * self.size + j] for j in range(self.size)]
            print(" | ".join(row))
            if i < self.size - 1:
                print("-" * (self.size * 4 - 3))

    def update(self, move, player):
        index = move - 1
        if 0 <= index < self.total and self.cells[index] == " ":
            self.cells[index] = player
            return True
        return False

    def check_winner(self, player):
        N = self.size
        for i in range(N):
            if all(self.cells[i * N + j] == player for j in range(N)):
                return True
            if all(self.cells[j * N + i] == player for j in range(N)):
                return True
        if all(self.cells[i * N + i] == player for i in range(N)):
            return True
        if all(self.cells[i * N + (N - 1 - i)] == player for i in range(N)):
            return True
        return False

    def is_tie(self):
        return all(cell != " " for cell in self.cells)

    def to_string(self):
        return ",".join(self.cells)

    def from_string(self, s):
        self.cells = s.split(",")

def main():
    host = input("Enter host to bind (default: localhost): ") or "localhost"
    port = 12345
    size = int(input("Enter board size: "))
    board = Board(size)

    #socket setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Server started on {host}:{port}, waiting for connection...")
    conn, addr = server.accept()
    print(f"Player O connected from {addr}")

    #sending board size
    conn.send(str(size).encode())

    current_player = "X"

    while True:
        board.display()

        if current_player == "X":
            try:
                move = int(input("Your move (Player X): "))
            except ValueError:
                print("Invalid input.")
                continue
            if not board.update(move, "X"):
                print("Invalid move. Try again.")
                continue
        else:
            #sends the board and waits for move from client
            conn.send(board.to_string().encode())
            move = int(conn.recv(1024).decode())
            if not board.update(move, "O"):
                print("Player O made an invalid move.")
                conn.send("INVALID".encode())
                continue

        #checks for win or tie
        if board.check_winner(current_player):
            board.display()
            result = f"WIN:{current_player}"
            conn.send(board.to_string().encode())
            conn.send(result.encode())
            print(f"Player {current_player} wins!")
            break
        elif board.is_tie():
            board.display()
            conn.send(board.to_string().encode())
            conn.send("TIE".encode())
            print("It's a tie!")
            break
        else:
            #sends the updated board state
            conn.send(board.to_string().encode())

        current_player = "O" if current_player == "X" else "X"

    conn.close()
    server.close()

if __name__ == "__main__":
    main()
