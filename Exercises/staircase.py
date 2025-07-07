def create_board():
    return [["#" for _ in range(3)] for _ in range(3)]

def print_board(board):
    print("---------")
    for row in board:
        print(" | ".join(row))
        print("---------")

def make_move(board, move_num):
    while True:
        try:
            move = input("Enter x y coordinates (1-3): ").split()
            x = int(move[0]) - 1
            y = int(move[1]) - 1

            if 0 <= x <= 2 and 0 <= y <= 2:
                if board[x][y] == "#":
                    board[x][y] = "X" if move_num % 2 == 1 else "O"
                    return board, move_num + 1
                else:
                    print("That space is already taken. Try again.")
            else:
                print("Coordinates must be between 1 and 3.")
        except (ValueError, IndexError):
            print("Invalid input. Enter two numbers between 1 and 3 separated by space.")

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "#":
            print(f"{board[i][0]} WON!")
            return True
        if board[0][i] == board[1][i] == board[2][i] != "#":
            print(f"{board[0][i]} WON!")
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "#":
        print(f"{board[0][0]} WON!")
        return True
    if board[0][2] == board[1][1] == board[2][0] != "#":
        print(f"{board[0][2]} WON!")
        return True

    return False

# Game loop
board = create_board()
move_num = 1

print_board(board)
for _ in range(9):
    board, move_num = make_move(board, move_num)
    print_board(board)
    if check_winner(board):
        break
else:
    print("It's a tie!")