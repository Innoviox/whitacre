from dataclasses import dataclass
import time
import random
import enum
import string
import tkinter as tk

SHAPES = [ # top -> bottom, ignore trailing zeros please
    [
        [[1], [1], [1], [1]],
        [[1, 1, 1, 1]]
    ],
    [
        [[1, 1], [1, 1]]
    ],
    [
        [[1], [1, 1], [1]],
        [[1, 1, 1], [0, 1]],
        [[0, 1], [1, 1], [0, 1]],
        [[0, 1], [1, 1, 1]]
    ],
    [
        [[1], [1], [1, 1]],
        [[0, 1], [0, 1], [1, 1]],
        [[1, 1, 1], [1]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[1], [1, 1, 1]],
        [[1, 1], [0, 1], [0, 1]],
        [[1, 1], [1], [1]]
    ],
    [
        [[1], [1, 1], [0, 1]],
        [[0, 1, 1], [1, 1]],
        [[0, 1], [1, 1], [1]],
        [[1, 1], [0, 1, 1]]
    ]
]

COLORS = list(string.ascii_uppercase)
EMPTY = ' '

class Direction(enum.Enum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    UP = 4

    @property
    def rotation(self):
        match self:
            case Direction.LEFT:
                return -1
            case Direction.RIGHT:
                return 1
        raise NotImplemented()
    

@dataclass
class Tile:
    x: int
    y: int
    shapes: list[list[int]]
    color: str
    # color: list[list[str]] = []
    rotation: int = 0

    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     for i, row in enumerate(self.sha
        

    def move(self, direction, board):
        match direction:
            case Direction.LEFT:
                if self.x == 0:
                    return False
                
                for y_delta in range(len(self.shape)):
                    non_zero_idx = 0
                    if 0 in self.shape[y_delta]:
                        while self.shape[y_delta][non_zero_idx] == 0:
                            non_zero_idx += 1
                    
                    if board.board[board.rows - self.y - y_delta - 1][self.x - 1 + non_zero_idx] != EMPTY:
                        return False

                self.x -= 1
                return True
            case Direction.RIGHT:
                for y_delta, x_delta in enumerate(self.shape):
                    x = self.x + len(x_delta)
                    if x >= board.cols:
                        return False
                    if board.board[board.rows - self.y - y_delta - 1][x] != EMPTY:
                        return False

                self.x += 1
                return True
            case Direction.DOWN:
                if self.y == 0:
                    return False

                for y_delta, x_delta in enumerate(self.shape[::-1]):
                    for xd in range(len(x_delta)):
                        x = self.x + xd
                        y = board.rows - self.y - y_delta
                        if y < 0 or x_delta[xd] == 0:
                            continue
                        if x >= board.cols:
                            continue
                        if board.board[y][x] != EMPTY:
                            return False                    
                self.y -= 1
                return True
            case Direction.UP:
                raise NotImplemented()

    def rotate(self, direction, board):
        old_rotation = self.rotation
        self.rotation = (self.rotation + direction.rotation) % len(self.shapes)
        # this code fuckin sucks
        try:
            Board.fix_tile_to_board(self, [i[:] for i in board.board[:]])
            return True
        except IndexError:
            sx = self.x
            for xd in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5]:
                self.x = sx + xd
                if not 0 <= self.x < board.cols:
                    continue
                try:
                    Board.fix_tile_to_board(self, [i[:] for i in board.board[:]])
                    return True
                except IndexError:
                    pass
        self.rotation = old_rotation
        return False                   

    @property
    def shape(self):
        return self.shapes[self.rotation]

class Board:
    def __init__(self):
        self.rows = 20
        self.cols = 11

        self.board = []
        self.initialize_board()

        self.tile = None

    def initialize_board(self):
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[-1].append(EMPTY)

    def display(self):
        disp = [i[:] for i in self.board[:]]
        
        if self.tile:
            Board.fix_tile_to_board(self.tile, disp)
            
        # print('\n'.join(('|' + ''.join(i) + '|') for i in disp))
        return disp

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

    def take_input(self, char):
        if not self.tile:
            return

        match char:
            case 'd':
                self.tile.move(Direction.RIGHT, self)
            case 'a':
                self.tile.move(Direction.LEFT, self)
            case 's':
                while self.tile.move(Direction.DOWN, self):
                    pass
            case 'z':
                self.tile.rotate(Direction.LEFT, self)
            case 'x':
                self.tile.rotate(Direction.RIGHT, self)

    def tick(self):
        if self.tile is None:
            self.spawn_tile()
            
        # move tile down
        if not self.tile.move(Direction.DOWN, self):
            self.fix_tile_to_board(self.tile, self.board)
            self.tile = None

        # check for tetrises
        tetrii = []
        for idx, row in enumerate(self.board):
            if all(i != EMPTY for i in row):
                print("TETRIS!")
                tetrii.append(idx)

        for idx in tetrii:
            self.board.pop(idx)
            self.board.insert(0, [EMPTY for _ in range(self.cols)])
            
    @staticmethod
    def fix_tile_to_board(tile, board): # modifies in-place
        for idx, length in enumerate(tile.shape[::-1]):
            y = tile.y + idx
            if y < len(board):
                for x_add in range(len(length)):
                    if length[x_add] != 0:
                        board[len(board) - y - 1][tile.x + x_add] = tile.color

class Game(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.board = Board()

        self.mainframe = tk.Frame()
        self.mainframe.pack()

        self.labels = []
        for row in range(self.board.rows):
            self.mainframe.grid_rowconfigure(row, minsize=30)
            self.labels.append([])
            for col in range(self.board.cols):
                self.mainframe.grid_columnconfigure(col, minsize=30)
                label = tk.Label(master=self.mainframe, text=" ", background="white", borderwidth=2, relief="raised")
                label.grid(row=row, column=col, sticky="news")
                self.labels[-1].append(label)
        
        self.speed = 1000

        self.bind("<KeyRelease>", self.handle_input)

    def start(self):
        self.tick()

    def tick(self):
        self.board.tick()
        self.update_view()
        self.after(self.speed, self.tick)

    def update_view(self):
        d = self.board.display()
        for r, row in enumerate(self.labels):
            for c, label in enumerate(row):
                label.config(text=d[r][c])

    def handle_input(self, e):
        self.board.take_input(e.char)
        self.update_view()

if __name__ == "__main__":
    g = Game()
    g.start()
    g.mainloop()
