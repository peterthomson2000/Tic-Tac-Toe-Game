from dataclasses import dataclass, field

@dataclass
class TicTacToeBoard:
    state: str = "is_playing"
    player: str = "X"
    positions: list[str] = field(default_factory=lambda: [""] * 9)

    def is_my_turn(self, i_am: str) -> bool:
        return i_am.lower() == self.player.lower()

    def make_move(self, index: int) -> bool:
        if self.positions[index] == "" and self.state == "is_playing":
            self.positions[index] = self.player
            self.check_winner()
            if self.state == "is_playing":
                self.switch_player()
            return True
        return False

    def switch_player(self):
        self.player = "O" if self.player == "X" else "X"

    def check_winner(self):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in wins:
            if self.positions[a] and self.positions[a] == self.positions[b] == self.positions[c]:
                self.state = f"{self.positions[a]}_won"
                return
        if all(pos != "" for pos in self.positions):
            self.state = "tie"

    def print_board(self):
        # The board has 9 positions: 0 to 8
        # We'll print 3 rows: top (0–2), middle (3–5), bottom (6–8)

        for start_index in [0, 3, 6]:  # Start of each row
            # Get each of the 3 positions in the current row
            first = self.positions[start_index] or " "
        second = self.positions[start_index + 1] or " "
        third = self.positions[start_index + 2] or " "

        # Print the row in the format: X |   | O
        print(f" {first} | {second} | {third} ")

        # Print the row divider if it's not the last row
        if start_index != 6:
            print("---+---+---")