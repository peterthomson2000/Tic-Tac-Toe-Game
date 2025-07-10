from tic_tac_toe_board import TicTacToeBoard
import time

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
    print("Welcome to Tic-Tac-Toe Multiplayer!")

    # Ask for player identity
    player = input("Are you Player X or O? ").strip().upper()
    if player not in ["X", "O"]:
        print("Invalid player. Must be X or O.")
        return

    # Load shared board
    board = TicTacToeBoard.load_from_redis()

    # Optionally reset game if it's over
    if board.state in ["won", "draw"]:
        choice = input("Previous game is over. Reset board? (y/n): ").lower()
        if choice == "y":
            board.reset()
            print("Board reset.")

    # Game loop
    while board.state == "is_playing":
        board = TicTacToeBoard.load_from_redis()
        board.print_board()

        if board.is_my_turn(player):
            print(f"It's your turn, Player {player}.")
            move = get_valid_move(player, board.positions)
            if board.make_move(move):
                result = board.check_winner()
                board.save_to_redis()

                if result in ["X", "O"]:
                    board.print_board()
                    print(f"Player {result} wins!")
                    break
                elif result == "Draw":
                    board.print_board()
                    print("It's a draw!")
                    break

                board.switch_turn()
                board.save_to_redis()
        else:
            print(f"Waiting for Player {board.player}...")
            time.sleep(1)

if __name__ == "__main__":
    main()