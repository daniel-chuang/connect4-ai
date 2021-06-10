"""
The minimax agent for the Connect4 game.

Imported into the game.

The algorithm is a recursive function, which has a controllable depth. 
"""

import numpy as np
import functools
import sys
import time
import copy

def recursionlimit():
    sys.setrecursionlimit(9999)

def actions(board):
    """
    Returns all possible moves
    """
    lst = []
    for index in range(len(board.matrix[0])):
        if board.matrix[0][index] == 0:
            lst.append(index)
    return lst

def result(board, action):
    """
    Returns the board and player that results from making move (i, j) on the board.
    """
    if action >= board.WIDTH or action <= -1:
        print("Invalid Action has been Passed")
        pass
    else:
        for i in range(board.HEIGHT - 1, -1, -1):
            if board.matrix[i, action] == 0:
                board.matrix[i, action] = board.player
                if board.player == 1:
                    board.player = 2
                else:
                    board.player = 1
                break
    return board

def winner(board):
    matrixList = [board.matrix, np.transpose(board.matrix)] # board.matrix for rows, np.transpose(board.matrix) for columns
    #matrixList.append(np.diag(board.matrix, k=0))
    #matrixList.append(np.diag(np.rot90(board.matrix)))

    # Check vertical / horizontal four in a row
    for matrix in matrixList:
        for row in matrix:
            count = 0 # how many times something appears in a row
            val = 0 # what is appearing

            for element in row:
                element = int(element)
                if element == val:
                    count += 1
                    if count >= board.in_a_row and val != 0:
                        # print(f"Player {val} Wins")
                        return val
                else:
                    val = element
                    count = 1
    
    # Check for diagonal 4 in a row
    diagMatrixList = []
    diagonals = []

    for matrix in [board.matrix, np.rot90(board.matrix)]:
        for k in range(-matrix.shape[0] + 1, matrix.shape[1]):
            diagonals.append(np.diag(matrix, k=k))
    
    for row in diagonals:
        count = 0 # how many times something appears in a row
        val = 0 # what is appearing

        for element in row:
            element = int(element)
            if element == val:
                count += 1
                if count >= board.in_a_row and val != 0:
                    # print(f"From agent: Player {val} has four in a row!")
                    return val
            else:
                val = element
                count = 1
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for a win
    if winner(board) != None:
        return True

    # Check for a tie
    elif np.count_nonzero(board.matrix) == board.WIDTH * board.HEIGHT: # checks if the matrix has a full grid
        print(f"The board is full, so this game is a tie!")
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 1:
        return 1
    elif winner(board) == 2:
        return -1
    else:
        return 0

"""
function negamax(node, depth, color) is
    if depth = 0 or node is a terminal node then
        return color × the heuristic value of node
    value := −∞
    for each child of node do
        value := max(value, negamax(child, depth − 1, −color))
    return −value
"""

# negamax 
def minimax(board, depth=0, player = -1, actions_path = []):

    # Return utility if the search has reached it's depth
    if depth == 5:
        return (actions_path[-1], utility(board))

    # Return utility if the game is over
    if board.movesMade() == board.WIDTH * board.HEIGHT or terminal(board):
        ## print(f"Path of Actions: {actions_path}, UTILITY: {utility(board)}")
        ## print(board.matrix)
        ## print(actions_path[-1])
        try:
            return (actions_path[-1], utility(board))
        except IndexError:
            return (None, utility(board))

    # -------------------- TREE SEARCH ---------------------
    # Set up a comparitor which stores the "best" utility values
    if player == -1:
        comparitor = 999
    else:
        comparitor = -999

    actions_list = list()
    for action in actions(board): # for every possible action in the frontier

        tempboard = copy.deepcopy(board)
        actions_path.append(action)
        
        if player == -1:
            comparitor_new = min(comparitor, minimax(result(tempboard, action), depth + 1, -player, actions_path)[1])
        else:
            comparitor_new = max(comparitor, minimax(result(tempboard, action), depth + 1, -player, actions_path)[1])

        actions_path.pop()

        if comparitor_new != comparitor:
            actions_list.append(action)

            comparitor = comparitor_new

    # return the best action, as well as the comparitor value
    # print(f"Path of Actions: {actions_path}, Comparitor Value : {-comparitor}")
    # print(board.matrix)
    return (actions_list[-1] + 1, comparitor)