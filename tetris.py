from dataclasses import dataclass
import time
import random
import enum

SHAPES = [ # top -> bottom
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
    ]
]

COLORS = 'RYGO' # red, yellow, green, orange
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
    rotation: int = 0

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
                    
                    if board[len(board) - self.y - y_delta - 1][self.x - 1 + non_zero_idx] != EMPTY:
                        return False

                self.x -= 1
                return True
            case Direction.RIGHT:
                for y_delta, x_delta in enumerate(self.shape):
                    x = self.x + len(x_delta)
                    if x >= len(board[0]):
                        return False
                    if board[len(board) - self.y - y_delta - 1][x] != EMPTY:
                        return False

                self.x += 1
                return True
            case Direction.DOWN:
                if self.y == 0:
                    return False

                for y_delta, x_delta in enumerate(self.shape[::-1]):
                    for xd in range(len(x_delta)):
                        x = self.x + xd
                        y = len(board) - self.y - y_delta
                        if y < 0 or x_delta[xd] == 0:
                            continue
                        if x >= len(board[0]):
                            return False
                        if board[y][x] != EMPTY:
                            return False                    
                self.y -= 1
                return True
            case Direction.UP:
                raise NotImplemented()

    def rotate(self, direction, board):
        self.rotation = (self.rotation + direction.rotation) % len(self.shapes)
        # todo check for room, move to fit if possible, if impossible don't rotate

    @property
    def shape(self):
        return self.shapes[self.rotation]

class Board:
    def __init__(self):
        self.rows = 20
        self.cols = 5

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
            
        print('\n'.join(('|' + ''.join(i) + '|') for i in disp))

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
        if not self.tile:
            return
        
        x = input()
        match x:
            case 'd':
                self.tile.move(Direction.RIGHT, self.board)
            case 'a':
                self.tile.move(Direction.LEFT, self.board)
            case 's':
                while self.tile.move(Direction.DOWN, self.board):
                    pass
            case 'z':
                self.tile.rotate(Direction.LEFT, self.board)
            case 'x':
                self.tile.rotate(Direction.RIGHT, self.board)

    def tick(self):
        # move tile down
        if not self.tile.move(Direction.DOWN, self.board):
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
        for idx, length in enumerate(tile.shape):
            y = tile.y + idx
            if y < len(board):
                for x_add in range(len(length)):
                    if length[x_add] != 0:
                        board[len(board) - y - 1][tile.x + x_add] = tile.color


b = Board()
b.start_game()
