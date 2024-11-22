from dataclasses import dataclass
import random

class Game:
    current_id = 0

    def __init__(self, name: str, board_size: int):
        self.board = Board(board_size) 
        self.name = name
        self.id = Game.current_id
        self.players = set()
        Game.current_id += 1 

class Board:
    square_pool = []
    
    @classmethod
    def load_squares():
        raise NotImplemented

    def __init__(self, size: int):
        squares = iter(random.choices(self.square_pool, k = size**2))
        self.squares = [
            [next(squares) for _ in range(5)]
            for _ in range(5)
        ]
    
    def mark(self, row, column, color):
        self.squares[row][column].color = color

    