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

    def from_string(self, s):
        self.cells = s.split(",")

def main():
    host = input("Enter server IP address (default: localhost): ") or "localhost"
    port = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except:
        print("Could not connect to server.")
        return

    size = int(client.recv(1024).decode())
    board = Board(size)
    print(f"Connected to server. Game size: {size}x{size}")
    print("You are Player O.")

    while True:
        board_data = client.recv(1024).decode()
        board.from_string(board_data)
        board.display()

        move = input("Your move (Player O): ")
        client.send(move.encode())

        board_data = client.recv(1024).decode()
        if board_data == "INVALID":
            print("Invalid move sent. Try again.")
            continue

        board.from_string(board_data)
        board.display()

        result = client.recv(1024).decode()
        if result.startswith("WIN"):
            winner = result.split(":")[1]
            print(f"Player {winner} wins!")
            break
        elif result == "TIE":
            print("It's a tie!")
            break

    client.close()

if __name__ == "__main__":
    main()
