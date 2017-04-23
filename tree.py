from sudoku_solver import SudokuSolver
"""
TO DO:

- stablo
- citanje iz txt file-a vise sudokua
- test na desetak sudoku-a
"""

class Tree(object):

    def __init__(self, name='root', children=None):
        self.solver = SudokuSolver()
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def main():

    tree = Tree()

if __name__ == "__main__":
    main()        