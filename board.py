import numpy as np

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