import numpy as np
import functools
import sys
from functools import cache, lru_cache

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
    if action > board.WIDTH or action <= -1:
        print("Invalid")
        pass
    else:
        action -= 1
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
                    if count >= board.in_a_row and val != 0:
                        print(f"Player {val} Wins")
                        return(val)
                else:
                    val = element
                    count = 1
    
    # Check for diagonal 4 in a row
    diagMatrixList = []
    diagonals = []

    for matrix in [board.matrix, np.rot90(board.matrix)]:
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
                if count >= board.in_a_row and val != 0:
                    print(f"Player {val} has four in a row!")
                    return val
            else:
                val = element
                count = 1

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

####### Minimax Algorithm #######

def max_value(board):
    """
    Returns the maximum utility value that a boardstate can provide, along with the action
    """
    # Set the original comparitor value to very low
    v = -999

    # If the board is terminal, return the utility value
    if terminal(board):
        return (utility(board), None)

    # Gets all possible utility values from min
    action_return = list()
    for action in actions(board):
        v_new = max(v, min_value(result(board, action))[0])
        if v_new != v:
            action_return.append(action)
        v = v_new
        if v == 1:
            break
    return (v, action_return[-1])

def min_value(board):
    """
    Returns the minimum utility value that a boardstate can provide, along with the action
    """
    # Set the original comparitor value to very high
    v = 999

    # If the board is terminal, return the utility value
    if terminal(board):
        return (utility(board), None)

    # Gets all possible utility values from max
    action_return = list()
    for action in actions(board):
        v_new = min(v, max_value(result(board, action))[0])
        if v_new != v:
            action_return.append(action)
        v = v_new
        if v == -1:
            break

    return (v, action_return[-1])

@cache
@lru_cache(maxsize=42)
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is terminal, then return None
    if terminal(board) == True:
        return None

    # Implement Minimax Algorithm
    if board.player == 1:
        return max_value(board)[1]
    else:
        return min_value(board)[1]