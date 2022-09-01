from dataclasses import dataclass
import time
import random

TILES = [
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

class Board:
    def __init__(self):
        self.rows = 10
        self.cols = 5

        self.board = []
        self.initialize_board()

        self.tile = None

    def initialize_board(self):
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[-1].append('B')

    def display(self):
        for row in self.board:
            for sq in row:
                print(sq, end='')
            print()

    def start_game(self):
        while not self.full():
            if self.tile is None:
                self.drop_tetris()
            # self.take_input()
            self.tick()

    def drop_tetris(self):
        shape = random.choice(TILES)

        self.tile = Tile(0, self.rows, shape)

    def full(self):
        ...

    def take_input(self):
        ...
        # todo rotate

    def tick(self):
        self.tile.y -= 1
        if self.tile.y == 0:
            self.fix_tile_to_board()
            self.tile = None
        

b = Board()
b.display()
