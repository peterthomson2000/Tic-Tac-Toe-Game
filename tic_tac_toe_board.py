from dataclasses import dataclass, field
import redis
import json

# Redis configuration
REDIS_HOST = "ai.thewcl.com"
REDIS_PORT = 6379
REDIS_PASSWORD = "atmega328"
STUDENT_NUMBER =   11 # Replace with your student number (0–13)
REDIS_KEY = f"tic_tac_toe:game_state:{STUDENT_NUMBER}"

# Redis client setup
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

@dataclass
class TicTacToeBoard:
    state: str = "is_playing"
    player: str = "X"
    positions: list[str] = field(default_factory=lambda: [" " for _ in range(9)])

    def is_my_turn(self, i_am: str) -> bool:
        return i_am.upper() == self.player

    def switch_turn(self):
        self.player = "O" if self.player == "X" else "X"

    def make_move(self, position: int) -> bool:
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
        if self.check_draw():
            return "Draw"
        return "None"

    def check_draw(self) -> bool:
        if " " not in self.positions:
            self.state = "draw"
            return True
        return False

    def print_board(self):
        p = self.positions
        print()
        print(f" {p[0]} | {p[1]} | {p[2]} ")
        print("---|---|---")
        print(f" {p[3]} | {p[4]} | {p[5]} ")
        print("---|---|---")
        print(f" {p[6]} | {p[7]} | {p[8]} ")
        print()

    # Redis: Serialize board to JSON string
    def serialize(self) -> str:
        return json.dumps({
            "state": self.state,
            "player": self.player,
            "positions": self.positions
        })

    # Redis: Save board state to Redis as JSON
    def save_to_redis(self):
        data = json.loads(self.serialize())
        r.json().set(REDIS_KEY, path='.', obj=data)

    # Redis: Load board state from Redis and return a TicTacToeBoard instance
    @classmethod
    def load_from_redis(cls):
        data = r.json().get(REDIS_KEY)
        if data:
            return cls(**data)
        else:
            return cls()  # Return a new board if nothing is in Redis

    # Reset board state and save to Redis
    def reset(self):
        self.positions = [" " for _ in range(9)]
        self.player = "X"
        self.state = "is_playing"
        self.save_to_redis()
        
        # ========================== Redis Setup Instructions ==========================
# 1. Import and configure the Redis client.
#    - Use the Redis host: ai.thewcl.com
#    - Port: 6379
#    - Password: atmega328
#    - Use your student number (0–13) as part of your key

# 2. Define a Redis key constant, for example:
#    REDIS_KEY = "tic_tac_toe:game_state"

# 3. Add a method: serialize(self)
#    - This should convert the current board object into a JSON string.

# 4. Add a method: save_to_redis(self)
#    - Converts the board to a dictionary using json.loads(self.serialize())
#    - Calls r.json().set(REDIS_KEY, path='.', obj=data)

# 5. Add a @classmethod: load_from_redis(cls)
#    - Loads the board data from Redis using r.json().get(REDIS_KEY)
#    - Returns a new TicTacToeBoard instance using cls(**data)

# 6. Add a method: reset(self)
#    - Resets the board: positions = [""] * 9, player = "X", state = "is_playing"
#    - Saves the reset board to Redis using save_to_redis()

# ==============================================================================