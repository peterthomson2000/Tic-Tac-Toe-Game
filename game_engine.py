from tic_tac_toe_board import TicTacToeBoard

def main():
    board = TicTacToeBoard()
    print("Welcome to Tic-Tac-Toe!")
    
    while board.state == "is_playing":
        board.print_board()
        print(f"Player {board.player}, choose a position (0-8):")

        try:
            pos = int(input("> "))
            if pos < 0 or pos > 8:
                print("Invalid position. Choose a number from 0 to 8.")
                continue

            if not board.make_move(pos):
                print("That position is already taken. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Final result
    board.print_board()
    if board.state == "tie":
        print("It's a tie!")
    else:
        print(f"Game over. {board.state.replace('_', ' ').capitalize()}!")

def main():
    print("Welcome to Tic-Tac-Toe!")
    board = TicTacToeBoard()
    board.print_board()
    main() #No need to call main() if this file is imported 