from dataclasses import dataclass
from os import PathLike
from typing import Union
import random
import json

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

    def save(self,dest):
        json.dump({'squares':
                   [[{
                       'player': s.player,
                       'goal': s.goal
                   } for s in row] for row in self.squares],
                   'size': self.size
                   },dest)

    @classmethod
    def load(cls, src):
        js = json.load(src)
        board = cls(1)
        board.squares = [
            [Square(**obj) for obj in row ]
            for row in js['squares']
        ]
        board.size = js['size']
        return board

@dataclass
class Square: 
    player: int | None
    goal: str
