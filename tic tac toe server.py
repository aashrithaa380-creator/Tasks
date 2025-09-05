import socket

class Board:
    def __init__(self, size):
        self.size = size
        self.total_cells = size * size
        self.cells = [" "] * self.total_cells

    def display(self):
        print("\nCurrent Board:")
        for i in range(self.size):
            row = [self.cells[i * self.size + j] for j in range(self.size)]
            print(" | ".join(row))
            if i < self.size - 1:
                print("-" * (self.size * 4 - 3))

    def update(self, cell, player):
        index = cell - 1
        if 0 <= index < self.total_cells and self.cells[index] == " ":
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

    def is_full(self):
        return all(cell != " " for cell in self.cells)

    def serialize(self):
        return ",".join(self.cells)

    def deserialize(self, data):
        self.cells = data.split(",")

# Main server function
def main():
    host = 'localhost'
    port = 12345

    size = int(input("Enter board size (e.g. 3): "))
    board = Board(size)

    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print("Waiting for player O to connect...")
    conn, addr = server.accept()
    print(f"Player O connected from {addr}")

    # Send board size to client
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
            print("Waiting for Player O's move...")
            conn.send(board.serialize().encode())  # send board
            move = int(conn.recv(1024).decode())
            if not board.update(move, "O"):
                print("Player O made an invalid move. Ending game.")
                break

        if board.check_winner(current_player):
            board.display()
            print(f"Player {current_player} wins!")
            conn.send(board.serialize().encode())
            conn.send(f"WIN:{current_player}".encode())
            break

        if board.is_full():
            board.display()
            print("It's a tie!")
            conn.send(board.serialize().encode())
            conn.send("TIE".encode())
            break

        current_player = "O" if current_player == "X" else "X"

    conn.close()
    server.close()

if __name__ == "__main__":
    main()
