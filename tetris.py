from dataclasses import dataclass
import time
import random

SHAPES = [
    '1111',
    '121',
    '22'
]

COLORS = 'RYGO' # red, yellow, green, orange

@dataclass
class Tile:
    x: int
    y: int
    shape: str
    color: str

class Board:
    def __init__(self):
        self.rows = 10
        self.cols = 5

        self.board = []
        self.initialize_board()

        self.tile = None

        self.heights = [0 for _ in range(self.cols)]

    def initialize_board(self):
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[-1].append('B')

    def display(self):
        disp = [i[:] for i in self.board[:]]
        
        if self.tile:
            Board.fix_tile_to_board(self.tile, disp)
            
        print('\n'.join(''.join(i) for i in disp))

    def start_game(self):
        while not self.full():
            self.display()
            if self.tile is None:
                self.spawn_tile()
            self.take_input()
            self.tick()

    def spawn_tile(self):
        self.tile = Tile(0, self.rows, random.choice(SHAPES), random.choice(COLORS))

    def full(self):
        ...

    def take_input(self):
        input()
        # todo rotate

    def tick(self):
        self.tile.y -= 1
        if self.tile.y == 0: # it can hit a tile on the board, todo
            self.fix_tile_to_board(self.tile, self.board)
            self.tile = None

    @staticmethod
    def fix_tile_to_board(tile, board): # modifies in-place
        for idx, length in enumerate(tile.shape):
            y = tile.y + idx
            if y < len(board):
                for x_add in range(int(length)):
                    board[len(board) - y - 1][tile.x + x_add] = tile.color

        

b = Board()
b.start_game()
