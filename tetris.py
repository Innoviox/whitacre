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
    color: str

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
        disp = [i[:] for i in self.board[:]]
        if self.tile:
            print(self.tile)
            for idx, length in enumerate(self.tile.shape):
                print(idx, length)
                y = self.tile.y + idx
                if y < len(disp):
                    for x_add in range(int(length)):
                        disp[len(disp) - y - 1][self.tile.x + x_add] = self.tile.color

        print('\n'.join(''.join(i) for i in disp))

    def start_game(self):
        while not self.full():
            self.display()
            if self.tile is None:
                self.drop_tetris()
            self.take_input()
            self.tick()

    def drop_tetris(self):
        shape = random.choice(TILES)

        self.tile = Tile(0, self.rows, shape, random.choice(COLORS))

    def full(self):
        ...

    def take_input(self):
        input()
        # todo rotate

    def tick(self):
        self.tile.y -= 1
        if self.tile.y == 0: # it can hit a tile on the board, todo
            # self.fix_tile_to_board()
            self.tile = None
        

b = Board()
b.start_game()
