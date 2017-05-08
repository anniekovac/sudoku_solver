'''
Created on 24. tra 2017.

@author: Annie
'''

import copy

from sudoku_solver import SudokuSolver

class SudokuTree(object):

    def __init__(self, tile, digit, sudoku_board, children=None):
        self.solver = SudokuSolver()
        self.solver.sudoku_board = copy.deepcopy(sudoku_board)
        self.tile = tile
        self.digit = digit
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        assert isinstance(node, SudokuTree)
        self.children.append(node)

