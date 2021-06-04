"""
Connect 4 Game
"""

# %% imports
import numpy as np
import pygame
import sys

# importing my board class
from board import board

# importing the agent
import agent
agent.recursionlimit()
sys.setrecursionlimit(9999)

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

        if board.player == 1:
            # Check for key events
            if event.type == pygame.KEYDOWN:
                if event.key in keyDict:
                    board.move(keyDict[event.key])
        
        else: #board.player has to be 2 then
            board.move(agent.minimax(board))

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
