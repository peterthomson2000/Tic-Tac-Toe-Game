from tic_tac_toe_board import TicTacToeBoard

def get_valid_move(player: str, board: list[str]) -> int:
    while True:
        move = input(f"Player {player}, choose a position (0-8): ")
        if not move.isdigit():
            print("> Invalid input. Please enter a number.")
            continue
        move = int(move)
        if move < 0 or move > 8:
            print("> Invalid range. Choose between 0 and 8.")
            continue
        if board[move] != " ":
            print("> That spot is taken. Choose another.")
            continue
        return move

def main():
    print("Welcome to Tic-Tac-Toe!")

    # Load board from Redis or create new one
    board = TicTacToeBoard.load_from_redis()

    # Print current state
    print("Current board:")
    board.print_board()

    # If the last game ended, offer to reset
    if board.state in ["won", "draw"]:
        choice = input("Previous game finished. Do you want to reset the board? (y/n): ").lower()
        if choice == 'y':
            board.reset()
            print("Board reset.")
            board.print_board()

    while board.state == "is_playing":
        move = get_valid_move(board.player, board.positions)
        board.make_move(move)
        result = board.check_winner()

        board.save_to_redis()  # Save after each move

        board.print_board()

        if result in ["X", "O"]:
            print(f"Player {result} wins!")
            break
        elif result == "Draw":
            print("It's a draw!")
            break

        board.switch_turn()
        board.save_to_redis()  # Save again after turn switch

if __name__ == "__main__":
    main()