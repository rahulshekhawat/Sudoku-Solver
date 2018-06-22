#!/usr/bin/env python3

"""
sudoku_solver.py:
This script creates an initial parent board from the user input,
then uses constraint propagation to create children boards and iterate
over them and uses recursion to create further children boards until
it either reaches a solution or backtracks to the last correct parent
board and iterates over it's next children board.

Input:
The input is a string of numbers consisting of sudoku values in row major form.
Empty sudko cells are to be filled with a value of 0 in input string.
The program will print out solved sudoku.
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

    # A list of of all 3x3 grids in a sudoku
    # where each 3x3 is a list of cells that it contains
    matrices_list = []
    for L in ('ABC', 'DEF', 'GHI'):
        for N in ('123', '456', '789'):
            temp = []
            for l in L:
                for n in N:
                    temp.append(l + n)
            matrices_list.append(temp)

    # A dictionary containing the cell positions as key and the 3x3 grid that
    # it belong to as it's value.
    # Dict[cell_position] = grid_list (if cell_position is in grid_list)
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
        # If a sudoku cell is already filled, then make sure that the row,
        # column, and 3x3 grid containing the cell don't have the same
        # value filled again.
        for pos in self.positions:
            value = self.board[pos]
            if value != 0:
                for neighbour in self.neighbours[pos]:
                    assert value != self.board[neighbour]
            else:
                pass

    def create_children(self):
        """
        This method generates and populates the self.children list with
        the children board for given board instance.

        Any given unfilled sudoku board can have only a single valid child
        board but its possible that we may fail to find the valid child
        using a simple constraints check. In this case the self.children
        is populated with a list of all the probable children.

        If the sudoku board is alread solved, then self.children will be
        an empty list. If the sudoku board is invalid (wrong choice made
        while filling a position) then self.children will be set to None.
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
                    # is a solution.
                    pass
        # If the for loop finished without returning a solution,
        # then the current board was a wrong choice
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Default input is an empty Sudoku board.
    parser.add_argument("-i", "--input",
                        help="Input the sudoku values in row major form. Enter 0\
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
    print("\nTime taken for solving given Sudoku: {0} Secs".
          format(stop - start))
