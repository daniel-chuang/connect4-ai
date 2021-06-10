"""
Connect 4 Game

2 Players: 1 Human, 1 AI (code in agent.py)

7 by 6 board. Win by connecting four pieces in a row.
"""

# Imports
import numpy as np
import pygame
import pygame.freetype # for fonts
import sys
import time

# Importing my board class
from board import board

# Importing the agent
import agent

# Board set up
board = board()

# Pygame set up
pygame.init()
pygame.display.set_caption(f"Loading Connect4") 
display = pygame.display.set_mode((board.WIDTH * board.BLOCKSIZE, board.HEIGHT * board.BLOCKSIZE))
pygame.display.flip()
crashed = False

# Caption set up
pygame.display.set_caption(f"Player {board.player} Going First. Agent Thinking...") 

# Font set up
font = pygame.freetype.Font("OpenSans-Regular.ttf", 25)
font.antialiased = True

# Key dictionary
keyDict = {pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4, pygame.K_5:5, pygame.K_6:6, pygame.K_7:7}

pygame.display.update()
time.sleep(1)

# Pygame Main Loop
while not crashed:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if board.player == 1:
            # Check for key events
            if event.type == pygame.KEYDOWN:
                if event.key in keyDict:
                    board.move(keyDict[event.key])
                    pygame.display.set_caption("Agent Thinking...") 
                    break

        # Prompt for minimax agent to play for player 2
        elif board.player == 2: # board.player has to be 2 then
            board.move(agent.minimax(board)[0])

        # Change the caption
        pygame.display.set_caption(f"Your Move") 

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
            if board.matrix[y, x] == 1: # drawing for  player 1
                pygame.draw.circle(display, (255, 0, 0), ((x + 0.5) * board.BLOCKSIZE, (y + 0.5) * board.BLOCKSIZE), board.BLOCKSIZE/2 - 4)

            elif board.matrix[y, x] == 2: # drawing for player 2
                pygame.draw.circle(display, (0, 0, 255), ((x + 0.5) * board.BLOCKSIZE, (y + 0.5) * board.BLOCKSIZE), board.BLOCKSIZE/2 - 4)

    # Checks for win
    # state: None = nothing, 0 = tie, 1 = p1 win, 2 = p2 win
    state = board.terminal()
    if state == 0: # In the case of a tie
        print(f"The board is full, so this game is a tie!")
        pygame.display.set_caption(f"The board is full, so this game is a tie!") 
        pygame.display.update()
        time.sleep(3)
        pygame.display.quit()
        sys.exit()
    elif state in [1, 2]: # In the case of a win
        print("from game1p.py")
        pygame.display.set_caption(f"Player {state} Wins") 
        print(f"Player {state} Wins")
        print(board)
        pygame.display.update()
        time.sleep(3)
        pygame.display.quit()
        sys.exit()

    pygame.display.update()
pygame.display.quit()
