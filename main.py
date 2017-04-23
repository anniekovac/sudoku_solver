import sys
import matplotlib.pyplot as plt
import os
from sudoku_solver import SudokuSolver
from tree import SudokuTree


def recursion(sudoku, tree):

    min_possibility = sudoku.find_min_possibilities()

    for idx in xrange(0, min_possibility[1]):
        x, y = min_possibility[0]

        try:
            new_sudoku = SudokuSolver()
            new_sudoku.sudoku_board = sudoku.sudoku_board
            new_sudoku.write_definite_solutions_loop()
            new_sudoku.tree_preprocessing()
            new_sudoku.check_valid_solutions(new_sudoku.sudoku_board)

            digit = sudoku.mark_up_board[x][y][idx]
            new_sudoku.sudoku_board[x][y] = digit
            new_sudoku.mark_up_board[x][y] = digit

            new_sudoku.write_definite_solutions_loop()
            new_sudoku.tree_preprocessing()

#            new_sudoku.plot_sudoku(new_sudoku.mark_up_board)
            
            new_sudoku.check_valid_solutions(new_sudoku.sudoku_board)

            new_child = SudokuTree(tile=(x,y), digit=digit, sudoku_board=new_sudoku.sudoku_board)
            tree.add_child(new_child)
#            new_sudoku.plot_sudoku(new_sudoku.mark_up_board)
            recursion(new_sudoku, new_child)

        except ValueError:
            if idx == min_possibility[1]-1:
                import pdb; pdb.set_trace()
                return
            continue


def main():
    sudoku = SudokuSolver()

    sudoku.check_valid_solutions(sudoku.sudoku_board)
    sudoku.write_definite_solutions_loop()
    sudoku.tree_preprocessing()
    min_possibility = sudoku.find_min_possibilities()


### SOLVING SUDOKU USING TREE

    tree = SudokuTree((-1, -1), 0, sudoku.sudoku_board)
    recursion(sudoku, tree)


if __name__ == "__main__":
    main()    