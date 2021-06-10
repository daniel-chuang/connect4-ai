"""
The class for the Connect4 board.
"""

import numpy as np
from random import randint

class board():

    """
    The class for the Connect4 board. Takes an input of WIDTH, HEIGHT, and BLOCKSIZE. However, these are all set to default values
    if not specified.

    Attributes:
    - board.player
    - board.in_a_row
    - board.WIDTH
    - board.HEIGHT
    - board.BLOCKSIZE
    - board.matrix

    Methods:
    - board.move(position)
    - board.movesMade()
    - board.terminal()
    """

    player = randint(1, 2) # starts with a random player
    in_a_row = 4                  # uses four in a row to check for win.

    def __init__(self, WIDTH=7, HEIGHT=6, BLOCKSIZE=20):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BLOCKSIZE = 50
        self.matrix = np.zeros((HEIGHT, WIDTH))

    def move(self, position):
        """
        Takes an position between 1 to 7 for which column to put a piece into. Puts the piece at the very lowest possible
        position in that respective column.
        """
        # Checks for if the position is between 1 to 7
        if position > self.WIDTH or position <= -1:
            print("Invalid")
            pass

        # If the input is valid, this runs
        else:
            position -= 1 # subtract one from the position for list indexing
            for i in range(self.HEIGHT - 1, -1, -1): # iterates from the very lowest position to the highest position
                if self.matrix[i, position] == 0: # if the position is open then put the piece there
                    self.matrix[i, position] = self.player
                    
                    # Switching to the next player
                    if self.player == 1:
                        self.player = 2
                    else:
                        self.player = 1
                    break

    def movesMade(self):
        """
        Returns the amount of moves that have been made by counting the amount of nonzero pieces in the matrix.
        """
        return np.count_nonzero(self.matrix[self.matrix != 0])

    def terminal(self):
        """
        Checks if the board has reached a terminal state (meaning that either the game has reached a tie, or someone has won).

        Returns the player number of the winner, if there is one. Otherwise, if terminal, returns 0. Finally, if a terminal state has
        not been reached, returns None.
        """
        matrixList = [self.matrix, np.transpose(self.matrix)] # self.matrix for rows, np.transpose(self.matrix) for columns

        # Check vertical / horizontal four in a row
        for matrix in matrixList:
            for row in matrix:
                count = 0 # how many times something appears in a row
                val = 0 # what is appearing

                for element in row:
                    element = int(element)
                    if element == val:
                        count += 1
                        if count >= self.in_a_row and val != 0:
                            return val
                    else:
                        val = element
                        count = 1
        
        # Check for diagonal 4 in a row
        diagMatrixList = []
        diagonals = []

        for matrix in [self.matrix, np.rot90(self.matrix)]:
            for k in range(-matrix.shape[0] + 1, matrix.shape[1]):
                #print(np.diag(matrix, k=k))
                diagonals.append(np.diag(matrix, k=k))
        
        for row in diagonals:
            count = 0 # how many times something appears in a row
            val = 0 # what is appearing

            for element in row:
                element = int(element)
                if element == val:
                    count += 1
                    if count >= self.in_a_row and val != 0:
                        return val
                else:
                    val = element
                    count = 1

        # Check for a tie
        if np.count_nonzero(self.matrix) == self.WIDTH * self.HEIGHT: # checks if the matrix has a full grid
            return 0
        
        return None
        
    def __repr__(self):
        return str(self.matrix)