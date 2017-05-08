'''
Created on 24. tra 2017.

@author: Annie
'''

import sys
import matplotlib.pyplot as plt
import os

class SudokuSolver(object):

    def __init__(self):

        self.valid_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.sudoku_board = [[0 for x in xrange(0,9)] for x in xrange(0,9)]                      
        self.read_sudoku_from_txt("sudoku.txt")

        self.mark_up_board = [[0 for x in xrange(0,9)] for x in xrange(0,9)]
        self.number_of_empty_tiles = len([x for sublist in self.sudoku_board \
                                          for element in sublist if element == 0])
        self.extract_column = lambda sudoku, column_index : [item[column_index] for item in sudoku]
        self.extract_row = lambda sudoku, row_index : sudoku[row_index]

    def find_min_possibilities(self):
        """
        Function for finding first tile with minimal 
        number of possibilities 
        in self.mark_up_board.

        return: 
                min_poss -- tuple ((row_index, column_index), length of tile)
        """
        min_poss = ((-1,-1), 9)
        for row_idx, row in enumerate(self.mark_up_board):
            for col_idx, col in enumerate(self.mark_up_board):
                tile = self.mark_up_board[row_idx][col_idx]
                if isinstance(tile, tuple) and (len(tile) < min_poss[1]) and (len(tile) > 1):
                    min_poss = ((row_idx, col_idx), len(tile))
        return min_poss

    def check_valid_solutions(self, board):
        """
        Checking if given solution for board has 
        inconsistent (wrong) solutions.
        """

        if any([any(row) for row in self.mark_up_board]) and not self.is_solved(self.mark_up_board):
            raise ValueError, "There is one blank space in mark_up_board!"

        extract_zeros = lambda group : [item for item in group if item != 0]
        for idx in xrange(0, len(self.valid_digits)):
            row = self.extract_row(board, idx)
            row = extract_zeros(row)
            if len(set(row)) < len(row):
                raise ValueError, "Invalid solution for row {}".format(idx)

            column = self.extract_column(board, idx)
            column = extract_zeros(column)
            if len(set(column)) < len(column):
                raise ValueError, "Invalid solution for column {}".format(idx)

            for idx_col in xrange(0, len(self.valid_digits)):
                submatrix = self.extract_sub(board, (idx, idx_col))
                submatrix = extract_zeros(submatrix)
                if len(set(submatrix)) < len(submatrix):
                    raise ValueError, "Invalid solution for sumbatrix"
        return True

    def is_solved(self, board):
        return all([all(row) for row in board])

    def read_sudoku_from_txt(self, file_path):
        """
        args:
                file_path - str (path to txt file with written sudokus)
        """
        with open(file_path, 'r') as file:
            board = []
            for line in file:
                line = line.strip(os.linesep)
                if line:
                    board.append([int(item) for item in line])
        self.sudoku_board = board


    def extract_sub(self, sudoku_board, pos):
        """
        Extracting sub-matrix of 3x3 elements from sudoku board.
        args:
            sudoku_board - list of lists (sudoku board from which 
                                          you want to extract submatrix)

            coordinates - tuple (x, y) - coordinates of tile
                                         from the board sudoku_board,
                                         they can be in range (0,0) --> (8,8)
        return:
            list (size 9)
        """
        int_division = lambda x : int((float(x)/float(3)))

        x, y = pos

        #looking for submatrix coordinates
        x_submat, y_submat = (int_division(x), int_division(y))

        submatrix = [ sudoku_board[y_submat*3 + i][x_submat*3 : x_submat*3 + 3] for i in xrange(0, 3)]
        flat_submatrix = [element for sublist in submatrix for element in sublist]
        return flat_submatrix

    def plot_sudoku(self, n):
        """
        Plotting sudoku grid n using matplotlib library.
        args:
            n - list of lists (sudoku grid 9x9)
        """
        plt.figure()
        for y in range(10):
            plt.plot([-0.05,9.05], [y, y], color='black', linewidth=1)
            
        for y in range(0,10,3):
            plt.plot([-0.05,9.05], [y, y], color='black', linewidth=3)
                
        for x in range(10):
            plt.plot([x, x], [-0.05, 9.05], color='black', linewidth=1)
        
        for x in range(0,10,3):
            plt.plot([x,x], [-0.05, 9.05], color='black', linewidth=3)

        plt.axis('image')
        plt.axis('off')

        for x in range(9):
            for y in range(9):
                digit = n[8 - y][x]
                if isinstance(digit, tuple):
                    #parsing tuple
                    digit = "".join(map(str, digit))
                plt.text(x + 0.1, y + 0.1, str(digit), fontsize=15)

        plt.show(block=False)
        #plt.pause(0.001)
        
    def find_empty(self):
        """
        Finding empty tile in sudoku, and marking it so 
        in the next iteration it is known not to pick that one.

        return
                tuple (coordinates of the empty tile)
        """
        length = len(self.valid_digits)
        for i in xrange(0, length):
            try:
                j = self.sudoku_board[i].index(0)
                self.sudoku_board[i][j] = "x"
                return (j, i)
            except ValueError:
                continue
        return (-1, -1)

    def find_possible_solution_for_tile(self, coordinates):
        """
        Finding possible solution(s) for tile given with coordinates 
        and writing that solution into self.mark_up_board as a tuple.
        """
        x, y = coordinates

        submatrix = self.extract_sub(self.sudoku_board, (x, y))
        row = self.extract_row(self.sudoku_board, y)
        column = self.extract_column(self.sudoku_board, x)

        #possible digits for this tile are the ones not in row, column or submatrix
        possible_digits = [item for item in self.valid_digits if item not in row + column + submatrix]

        #writing possible solutions into mark_up_board
        if possible_digits:
            self.mark_up_board[y][x] = tuple(possible_digits)


    def erase_markers(self):
        """
        Erasing markers "x" fromm self.sudoku_board and
        adding zeros to the right places on self.mark_up_board.
        """
        for i, row in enumerate(self.sudoku_board):
            for j, element in enumerate(row):
                if element == "x":
                    self.sudoku_board[i][j] = 0
                else:
                    if element != 0:
                        self.mark_up_board[i][j] = element

    def write_one_possible_solution(self, counter):
        """
        If there are some tiles that have only one possible 
        solution, this function will write them down in 
        self.sudoku_board matrix. Making the counter 
        smaller for 1 every time there is one number
        written in final sudoku board.
        args
            counter - int
        return
            counter - int
        """
        for i, row in enumerate(self.mark_up_board):
            for j, element in enumerate(row):
                if isinstance(element, tuple):
                    if len(element) == 1 and self.sudoku_board[i][j] == 0:
                        self.sudoku_board[i][j] = int(*element)
                        counter -= 1
        return counter

    def find_two_possibles_in_submatrix(self, index):
        """
        This function searches for pairs, triples or quadriples
        that appear in two, three, or four different tiles in submatrix.
        If pair of possible digits appears two times in submatrix,
        we know that we can eliminate those two digits from other tiles
        in that submatrix.
        """
        group = self.extract_sub(self.mark_up_board, index)
        group_sets = [set(item) for item in group if isinstance(item, tuple) and len(item) > 1]

        new_group_sets = []
        for sett in group_sets:
            if sett not in new_group_sets:
                new_group_sets.append(sett)

        for sett in new_group_sets:
            if group_sets.count(sett) != len(list(sett)):
                continue

            for digit in list(sett):
                possibles = [item for item in group if isinstance(item, tuple) and (digit in item) and set(item) != sett]
                for poss in possibles:
                    for i in xrange(0,9):
                        try:
                            j = self.mark_up_board[i].index(poss)
                            break
                        except ValueError:
                            continue
                    if self.extract_sub(self.mark_up_board, (j,i)) == group:
                        self.mark_up_board[i][j] = tuple([item for item in poss if item != digit])

    def find_two_possibles_in_group(self, index, which_group):
        """
        This function searches for pairs, triples or quadriples
        that appear in two, three, or four different tiles in group.
        If pair of possible digits appears two times in group,
        we know that we can eliminate those two digits from other tiles
        in that group.
        """        
        group_dict = {
        "row" : lambda : self.extract_row(self.mark_up_board, index),
        "column" : lambda : self.extract_column(self.mark_up_board, index)
        }

        group = group_dict[which_group]()
        group = [list(item) for item in group if isinstance(item, tuple)]

        group_sets = [set(item) for item in group]
        new_group_sets = []
        for sett in group_sets:
            if sett not in new_group_sets:
                new_group_sets.append(sett)

        for sett in new_group_sets:
            if group_sets.count(sett) != len(list(sett)):
                continue

            for digit in list(sett):
                for i, item in enumerate(group_dict[which_group]()):
                    item = [item] if isinstance(item, int) \
                            else list(item)
                    if digit in item and set(item) != sett:
                        if which_group == "column":
                            self.mark_up_board[i][index] = tuple([dig for dig in item if dig not in list(sett)])
                        elif which_group == "row":
                            self.mark_up_board[index][i] = tuple([dig for dig in item if dig not in list(sett)])

    def write_definite_solutions_loop(self):
        counter = self.number_of_empty_tiles

        #while there are empty tiles in final sudoku_board
        it = 0
        while counter:
            it += 1
            empty_coordinates = (-2, -2)
            while empty_coordinates != (-1,-1):
                empty_coordinates = self.find_empty()
                self.find_possible_solution_for_tile(empty_coordinates)

            self.erase_markers()
            counter = self.write_one_possible_solution(counter)

            #if number of iterations is bigger than 15, it means we're 
            #stuck in a loop, another algorithm needs to be implemented
            #for hard sudokus
            if it > 8:
                break

    def update_mark_up_board(self):
        """
        Updating values of self.mark_up_board by looking at
        certain solutions from self.sudoku_board. Eliminating
        impossible solutions from self.mark_up_board_tuples.
        """
        for i in xrange(0,9):
            for j in xrange(0,9):
                submatrix = self.extract_sub(self.sudoku_board, (j,i))
                row = self.extract_row(self.sudoku_board, i)
                column = self.extract_column(self.sudoku_board, j)

                possible_digits = [item for item in self.valid_digits if item not in row + column + submatrix]
                #writing possible solutions into mark_up_board
                if possible_digits and self.sudoku_board[i][j] == 0 and len(possible_digits) < len(self.mark_up_board[i][j]):
                    self.mark_up_board[i][j] = tuple(possible_digits)

    def tree_preprocessing(self):
        """
        Preprocessing for minimazing possible solutions to 
        speed up the tree.
        """

        self.update_mark_up_board()

        broj = 12
        while broj:
             
            for i in xrange(0, 9):
                self.find_two_possibles_in_group(i, "column")
                self.find_two_possibles_in_group(i, "row")

            for i in xrange(0,9):
                for j in xrange(0,9):
                    self.find_two_possibles_in_submatrix((j,i))

            for i in xrange(0,9):
                for j in xrange(0,9):
                    tile = self.mark_up_board[i][j]
                    if isinstance(tile, tuple) and len(tile) == 1:
                        self.mark_up_board[i][j] = tile[0]
                        if self.sudoku_board[i][j] == 0:
                            self.sudoku_board[i][j] = tile[0]


            if not self.number_of_empty_tiles:
                return

            broj -= 1
