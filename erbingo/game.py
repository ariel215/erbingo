from dataclasses import dataclass
from os import PathLike
from typing import Union
import random

class Game:
    current_id = 0

    def __init__(self, board_size: int):
        self.board = Board(board_size) 
        self.id = Game.current_id
        self.players = set()
        Game.current_id += 1 

class Board:
    square_pool = []
    
    @classmethod
    def load_squares(cls, filename: Union[str, bytes, PathLike]):
        with open(filename,'r') as file:
            cls.square_pool = [
                line.strip() for line in file
            ]

    def __init__(self, size: int):
        squares = iter(random.sample(self.square_pool, k = size**2))
        self.squares = [
            [Square(None, next(squares)) for _ in range(size)]
            for _ in range(size)
        ]
        self.size = size
    

    def mark(self, row, column, color):
        self.squares[row][column].color = color

@dataclass
class Square: 
    player: int | None
    goal: str
