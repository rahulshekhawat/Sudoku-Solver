#!/usr/bin/env python3

"""
sudoku_solver.py:
This program uses constraint propogation and backtracking to solve any given
9x9 Sudoku.


Naming:
All the rows are numbered from A to I.
All the columns are numbered from 1 to 9
Each cell position is represented as row and column name: A6

Also, for any given unfilled Suoku board, it's child is a board derived from
it by filling an empty cell position using constraints.


Input:
The input to this program is a string of all values for each position starting
from first row to the last row. Empty cells are filled with value 0.
The program will automatically convert string input to integers and print out
the solved sudoku after solving it.

Average time for solving worst case scenario (empty sudoku) - 0.02 secs
"""

__author__ = "Rahul Shekhawat"
__copyright__ = ""
__credits__ = "[Rahul Shekhawat]"
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Rahul Shekhawat"
__email__ = "rahul.shekhawat.dev.mail@gmail.com"
__status__ = "Release"


import time
import copy
import argparse


def elements_of_sudoku():

    # A list of all 3x3 grid's lists on the Sudoku board
    # Each 3x3 grid list contains the position name for each cell in grid.
    # [[3x3 grid], [3x3 grid], ...]
    matrices_list = []
    for L in ('ABC', 'DEF', 'GHI'):
        for N in ('123', '456', '789'):
            temp = []
            for l in L:
                for n in N:
                    temp.append(l + n)
            matrices_list.append(temp)

    # A dictionary containing the cell positions as key and 3x3 grid list that
    # it belong to as it's value.
    # Dict[cell_position] = grid_list (if cell_position in grid_list)
    matrices = {}
    for letter in 'ABCDEFGHI':
        for num in '123456789':
            key = letter + num
            for matrix in matrices_list:
                if key in matrix:
                    matrices[key] = matrix

    # A list of all cell positions on Sudoku board in alphabetical order
    positions = []
    for letter in 'ABCDEFGHI':
        for num in '123456789':
            positions.append(letter + num)

    # A dictionary containing all cell position as it's keys and the value is
    # a list of all cell positions in a row, column, and 3x3 grid to which
    # constraints apply for the given cell position.
    neighbours = {}
    for letter in 'ABCDEFGHI':
        for num in '123456789':
            row = set([letter + n for n in '123456789'])
            column = set([l + num for l in 'ABCDEFGHI'])
            matrix = set(matrices.get(letter + num))
            neighbours[letter + num] = list((row | column | matrix) -
                                            set([letter + num]))

    return matrices, positions, neighbours


class Board:

    matrices, positions, neighbours = elements_of_sudoku()

    def __init__(self, board):
        self.board = board
        self._assert_board_is_correct()
        self.children = []

    def _assert_board_is_correct(self):
        # If a cell is filled with some value, assert that none of the rows,
        # columns, and 3x3 grids have the same value.
        for pos in self.positions:
            value = self.board[pos]
            if value != 0:
                for neighbour in self.neighbours[pos]:
                    assert value != self.board[neighbour]
            else:
                pass

    def create_children(self):
        """
        A given unfilled sudoku can have only 1 valid child board. But in case
        the valid child cannot be found using constraints, a list of possible
        valid children is generated and returned.

        If the Sudoku board cannot have any possible children because it is
        already solved, then self.children will be an empty list.
        If it is because the sudoku board is invalid (wrong choice made while
        filling a position) then self.children will contain a single
        'None' element.
        """

        # No need to search for a child if the Sudoku is already solved.
        if self.board_is_solved():
            return
        else:
            # Options contains position as 'key' and a SET of possible numbers
            # that can be filled in that position as 'value'
            options = {}
            full_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

            # Check if you can find a child just by normal constraint check
            for pos in self.positions:
                if self.board[pos] != 0:
                    options[pos] = set()
                else:
                    neighbour_values = []
                    for neighbour in self.neighbours[pos]:
                        neighbour_values.append(self.board[neighbour])
                    options[pos] = full_set - set(neighbour_values)
                    # Check if there is an unassigned box/position with no
                    # possibility (child fail)
                    if len(options[pos]) == 0:
                        self.children.append(None)
                        return
                    # If only 1 possibility, valid child
                    elif len(options[pos]) == 1:
                        child_board = copy.copy(self.board)
                        child_board[pos] = options[pos].pop()
                        child = Board(board=child_board)
                        self.children.append(child)
                        return
                    else:
                        pass

            # If you can't find child by normal means then it is
            # time to create multiple children by filling random possiblities

            # Step-1: Find a position on board with minimum possibilities
            # to fill
            pos_options = {}
            for key in options:
                # If options[key] evaluates to false, it means that it is an
                # empty set because position is already filled. Which means we
                # cannot pick minimum possibilty item for/from that position.
                if options[key]:
                    pos_options[key] = options[key]
                else:
                    pass
            min_posiblity_pos = min(pos_options, key=lambda x: len(pos_options[x]))

            # Step-2: Create a child from each possibility of that box
            for i in range(len(pos_options[min_posiblity_pos])):
                child_board = copy.copy(self.board)
                child_board[min_posiblity_pos] = options[min_posiblity_pos].pop()
                child = Board(board=child_board)
                self.children.append(child)

    def board_is_solved(self):
        for pos in self.positions:
            # If the board contains any unfilled cell
            if self.board[pos] == 0:
                return False
        # If all the cells in the board have been filled
        return True


def solve_board(board):
    temp = board

    if temp.board_is_solved():
        return temp
    else:
        board.create_children()
        for i in range(len(board.children)):
            temp = board.children[i]
            if temp is None:
                return None
            else:
                solution = solve_board(temp)
                if solution is not None:
                    return solution
                else:
                    # Pass because you need to check if the next child
                    # of board is the correct answer
                    pass
        # If the for loop finished without returning a solution
        # then it means that board was a wrong choice
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Default input is an empty Sudoku board.
    parser.add_argument("-i", "--input",
                        help="Input the sudoku rows top to bottom. Enter 0\
                        for empty cells. e.g.-  501403....708",
                        default='0' * 81)

    args = parser.parse_args()
    if len(args.input) == 81:
        pass
    else:
        print("Input doesn't equal 81 characters. Try again")
        exit()

    start = time.time()
    positions = elements_of_sudoku()[1]
    i = iter(args.input)
    board = {}
    try:
        for pos in positions:
            board[pos] = int(next(i))
    except ValueError:
        print("Invalid input")
    sudoku_board = Board(board=board)
    solution = solve_board(sudoku_board)
    if solution is None:
        print("No possible solution found. Entered input might be invalid.")
    else:
        for key in sorted(solution.board):
            print(key, ':', solution.board[key], sep='', end='   ')

    stop = time.time()
    print("\nTime consumed for solving given Sudoku: {0} Secs".
          format(stop - start))
