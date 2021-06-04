"""
Connect 4 Game
"""

# %% imports
import numpy as np
import pygame
import sys

# importing my board class
from board import board

# %% Set up board class
class board():

    def __init__(self, WIDTH=7, HEIGHT=6, BLOCKSIZE = 20):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BLOCKSIZE = 50
        self.matrix = np.zeros((HEIGHT, WIDTH))
        self.player = 1
        self.in_a_row = 4

    def move(self, position):
        if position > self.WIDTH or position <= -1:
            print("Invalid")
            pass
        else:
            position -= 1
            for i in range(self.HEIGHT - 1, -1, -1):
                if self.matrix[i, position] == 0:
                    self.matrix[i, position] = self.player
                    if self.player == 1:
                        self.player = 2
                    else:
                        self.player = 1
                    break

    def movesMade(self):
        return np.count_nonzero(self.matrix[self.matrix != 0])

    def terminal(self):
        matrixList = [self.matrix, np.transpose(self.matrix)] # self.matrix for rows, np.transpose(self.matrix) for columns
        #matrixList.append(np.diag(self.matrix, k=0))
        #matrixList.append(np.diag(np.rot90(self.matrix)))

        """
        print("Diagonal")
        print(matrixList)
        """

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
                            print(f"Player {val} Wins")
                            pygame.display.quit()
                            sys.exit()
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
                        print(f"Player {val} Wins")
                        pygame.display.quit()
                        sys.exit()
                else:
                    val = element
                    count = 1

        # Check for a tie
        if np.count_nonzero(self.matrix) == self.WIDTH * self.HEIGHT: # checks if the matrix has a full grid
            print(f"The board is full, so this game is a tie!")
            pygame.display.quit()
            sys.exit()
        
    def __repr__(self):
        return str(self.matrix)

# %% Board set up
board = board()
print(board)

# %% Pygame Set Up
pygame.init()
pygame.display.set_caption(f"Connect 4: {board.WIDTH} by {board.HEIGHT} Board")
display = pygame.display.set_mode((board.WIDTH * board.BLOCKSIZE, board.HEIGHT * board.BLOCKSIZE))
pygame.display.flip()
crashed = False

# Key dictionary
keyDict = {pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4, pygame.K_5:5, pygame.K_6:6, pygame.K_7:7}

# %% Pygame Main Loop
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
        # Check for key events
        if event.type == pygame.KEYDOWN:
            if event.key in keyDict:
                board.move(keyDict[event.key])
                print(board.matrix)

    # Draw horizontal gridlines
    for x in range(board.WIDTH + 1):
        pygame.draw.rect(display, (255, 255, 255),
                                            (0, x * board.BLOCKSIZE, (board.HEIGHT + 1) * board.BLOCKSIZE, 1))
    
    # Draw vertical gridlines
    for y in range(board.HEIGHT + 1):
        pygame.draw.rect(display, (255, 255, 255),
                                            (y * board.BLOCKSIZE, 0, 1, (board.WIDTH + 1) * board.BLOCKSIZE))

    # Draw pieces
    for x in range(board.WIDTH):
        for y in range(board.HEIGHT):
            if board.matrix[y, x] == 1:
                pygame.draw.circle(display, (255, 0, 0), ((x + 0.5) * board.BLOCKSIZE, (y + 0.5) * board.BLOCKSIZE), board.BLOCKSIZE/2 - 4)

            elif board.matrix[y, x] == 2:
                pygame.draw.circle(display, (0, 0, 255), ((x + 0.5) * board.BLOCKSIZE, (y + 0.5) * board.BLOCKSIZE), board.BLOCKSIZE/2 - 4)

    # Checks for win
    board.terminal()

    pygame.display.update()
pygame.display.quit()
# %%
