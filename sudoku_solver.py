import sys
import matplotlib.pyplot as plt
import pdb
import math

class SudokuSolver(object):

    def __init__(self):

        self.valid_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]


        self.sudoku_board = [[8, 0, 0, 0, 0, 4, 1, 0, 0],
                             [6, 0, 0, 0, 7, 0, 0, 0, 2],
                             [0, 0, 0, 0, 6, 1, 5, 0, 3],
                             [7, 0, 0, 0, 4, 0, 0, 0, 1],
                             [0, 9, 6, 0, 0, 0, 8, 4, 7],
                             [4, 1, 2, 0, 0, 5, 0, 3, 9],
                             [1, 5, 9, 8, 0, 3, 0, 0, 4],
                             [0, 6, 4, 1, 5, 7, 0, 0, 0],
                             [2, 0, 0, 0, 0, 6, 3, 0, 0]]

        self.mark_up_board = [[0 for x in xrange(0,9)] for x in xrange(0,9)]

        self.number_of_empty_tiles = len([x for sublist in self.sudoku_board \
                                          for element in sublist if element == 0])

        self.extract_column = lambda sudoku, column_index : [item[column_index] for item in sudoku]
        self.extract_row = lambda sudoku, row_index : sudoku[row_index]

    def extract_sub(self, sudoku, x, y):
        """
        Extracting sub-matrix of 3x3 elements from sudoku board.
        args:
            x, y - ints (coordinates)
        return:
            flat_submatrix - list (size 9)
        """
        # x = x//3
        int_division = lambda x : int((float(x)/float(3)))

        #looking for submatrix coordinates
        x_submat, y_submat = (int_division(x), int_division(y))

        #extracting submatrix and turning it into flat list
        submatrix = [ sudoku[y_submat*3 + i][x_submat*3 : x_submat*3 + 3] for i in xrange(0, 3)]
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
                    #a = "".join(map(str, a))
                    digit = "".join(str(digit).split("(", 1)[-1].rsplit(")",1)[0].split(", "))
                plt.text(x + 0.1, y + 0.1, str(digit), fontsize=15)
        plt.show()

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
        x, y = (coordinates)
        row = self.extract_row(self.sudoku_board, y)
        column = self.extract_column(self.sudoku_board, x)
        submatrix = self.extract_sub(self.sudoku_board, *coordinates)

        #possible digits for this tile are the ones not in row, column or submatrix
        possible_digits = [item for item in self.valid_digits if item not in row + column + submatrix]

        #writing possible solutions into mark_up_board
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
                    if len(element) == 1:
                        self.sudoku_board[i][j] = int(*element)
                        counter -= 1
        return counter

    def find_same_possibilities_in_group(self, index, which_group):
        if which_group == "row":
            group = self.extract_row(self.mark_up_board, index)
        elif which_group == "column":
            group = self.extract_column(self.mark_up_board, index)
        elif which_group == "submatrix":
            group = self.extract_sub(self.mark_up_board, *index)
        else:
            raise NameError, "Not specified name of the group you want to search"
        
        tuples = [temp for temp in group if isinstance(temp, tuple)]
        duplicates = [x for n, x in enumerate(tuples) if x in tuples[:n]]

        for item in duplicates:
            if tuples.count(item) == len(item):
                for digit in item: 
                    for i, element in enumerate(group):
                        if isinstance(element, tuple) and element != item:
                            group[i] = tuple([num for num in element if num != digit])
        return group

    def write_definite_solutions_loop(self):
        counter = self.number_of_empty_tiles

        #while there are empty tiles in final sudoku_board
        it = 0
        while counter:
            it += 1
            print "Counter: ", counter
            empty_coordinates = (-2, -2)
            while empty_coordinates != (-1,-1):
                empty_coordinates = self.find_empty()
                self.find_possible_solution_for_tile(empty_coordinates)

            self.erase_markers()
            counter = self.write_one_possible_solution(counter)
            
            #if number of iterations is bigger than 15, it means we're 
            #stuck in a loop, another algorithm needs to be implemented
            #for hard sudokus
            if it > 15:
                break


def main():
    sudoku = SudokuSolver()

### TRYING TO SOLVE SUDOKU USING ONLY CERTAIN SOLUTIONS
    
    
    sudoku.write_definite_solutions_loop()

### TRYING TO ELIMINATE IMPOSSIBLE SOLUTIONS FROM GROUPS
    
    for i in xrange(0, 9):
        new_row = sudoku.find_same_possibilities_in_group(i, "row")
        sudoku.mark_up_board[i] = new_row
        new_col = sudoku.find_same_possibilities_in_group(i, "column")
        for row_index, row in enumerate(sudoku.mark_up_board):
            sudoku.mark_up_board[row_index][i] = new_col[row_index]
            
#    sudoku.write_definite_solutions_loop()

    # print "Number of blank spaces in the beginning: ", sudoku.number_of_empty_tiles
    # print "Number of iterations: ", it
    sudoku.plot_sudoku(sudoku.sudoku_board)
#    sudoku.plot_sudoku(sudoku.mark_up_board)

if __name__ == "__main__":
    main()
