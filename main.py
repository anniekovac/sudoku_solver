'''
Created on 24. tra 2017.

@author: Annie Kovac
'''

from sudoku_solver import SudokuSolver
from tree import SudokuTree

import copy


def recursion(sudoku, tree, solved=False, solved_sudoku_board=None):
    if solved:
        return

    min_possibility = sudoku.find_min_possibilities()

    for idx in xrange(0, min_possibility[1]):
        #finding indexes of the board with minimal
        #number of possible solutions
        x, y = min_possibility[0]

        try:
            new_sudoku = SudokuSolver()
            new_sudoku.sudoku_board = copy.deepcopy(sudoku.sudoku_board)
            new_sudoku.write_definite_solutions_loop()
            new_sudoku.tree_preprocessing()

            #new_sudoku.plot_sudoku(new_sudoku.sudoku_board)
            new_sudoku.check_valid_solutions(new_sudoku.sudoku_board)

            digit = sudoku.mark_up_board[x][y][idx]
            new_sudoku.sudoku_board[x][y] = digit
            new_sudoku.mark_up_board[x][y] = digit

            new_sudoku.write_definite_solutions_loop()
            new_sudoku.tree_preprocessing()
            if new_sudoku.is_solved(new_sudoku.sudoku_board):

                if new_sudoku.check_valid_solutions(new_sudoku.sudoku_board):
                    new_sudoku.plot_sudoku(new_sudoku.sudoku_board)
                    solved = True

            #new_sudoku.plot_sudoku(new_sudoku.mark_up_board)

            new_sudoku.check_valid_solutions(new_sudoku.sudoku_board)
            #new_sudoku.plot_sudoku(new_sudoku.mark_up_board)
            new_child = SudokuTree(tile=(x,y), digit=digit, sudoku_board=new_sudoku.sudoku_board)
            tree.add_child(new_child)
            recursion(new_sudoku, new_child, solved)

        except ValueError:
            #this will happen if new_sudoku.sudoku_board
            #has some invalid solutions written
            if idx == min_possibility[1]-1:
                return
            continue


def main():
    sudoku = SudokuSolver()

    sudoku.check_valid_solutions(sudoku.sudoku_board)
    sudoku.write_definite_solutions_loop()
    sudoku.tree_preprocessing()


### SOLVING SUDOKU USING TREE

    tree = SudokuTree((-1, -1), 0, sudoku.sudoku_board)
    recursion(sudoku, tree)

    print "bla"


if __name__ == "__main__":
    main()    