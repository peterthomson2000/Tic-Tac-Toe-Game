from dataclasses import dataclass, field

@dataclass
class TicTacToeBoard:
    state: str = "is_playing"
    player: str = "X"
    positions: list[str] = field(default_factory=lambda: [" " for _ in range(9)])

    def is_my_turn(self, i_am: str) -> bool:
        return i_am.upper() == self.player

    def switch_turn(self):
        self.player = "O" if self.player == "X" else "X"

    def make_move(self, position: int):
        if self.positions[position] == " ":
            self.positions[position] = self.player
            return True
        return False

    def check_winner(self) -> str:
        p = self.positions
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in wins:
            if p[a] == p[b] == p[c] and p[a] != " ":
                self.state = "won"
                return p[a]
        if " " not in p:
            self.state = "draw"
            return "Draw"
        return "None"

    def print_board(self):  
        p = self.positions
        print()
        print(" " + p[0] + " | " + p[1] + " | " + p[2])
        print("---|---|---")
        print(" " + p[3] + " | " + p[4] + " | " + p[5])
        print("---|---|---")
        print(" " + p[6] + " | " + p[7] + " | " + p[8])
        print()