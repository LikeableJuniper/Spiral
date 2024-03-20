import functools
from vectors import Vector


class Matrix:
    def __init__(self, values, forceCheck=True):
        """
        Creates a Matrix. Expected data format is as follows: [[a11, a21, a31,..., am1], [a12, a22, a32,..., am2],..., [a1n, a2n, a3n,..., amn]]
        """
        self.values = values

        if forceCheck:
            self.rows, self.columns = len(values), len(values[0])
            
            for checkRow in values:
                if len(checkRow) != self.columns:
                    raise ValueError("Amount of columns isn't the same each row.")

    def __repr__(self):
        returnVal = ""
        for row in self.values:
            for val in row:
                returnVal += str(val) + " "
            returnVal += "\n"
        return returnVal[:-1] # Removes newline at the end of string

    def __getitem__(self, i):
        return self.values[i]
    
    def __setitem__(self, i, newVal):
        self.values[i] = newVal

    def __add__(self, other):
        if isinstance(other, Matrix):
            if not (self.rows == other.rows and self.columns == other.columns):
                raise ValueError("Matrix dimensions do not match.")
            finalMatrixValue = []

            #The following code is to prevent pythons weird behaviour with lists created using k*[[a, b, c]] where editing one sublist will edit all others.
            for row in range(self.rows):
                finalMatrixValue.append([])
                for column in range(self.columns):
                    finalMatrixValue[row].append(0)
            
            finalMatrix = Matrix(finalMatrixValue)

            for i in range(self.rows):
                for j in range(self.columns):
                    finalMatrix[i][j] = self[i][j] + other[i][j]
            
            return finalMatrix

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if not (self.rows == other.rows and self.columns == other.columns):
                raise ValueError("Matrix dimensions do not match.")
            finalMatrixValue = []

            #The following code is to prevent pythons weird behaviour with lists created using k*[[a, b, c]] where editing one sublist will edit all others.
            for row in range(self.rows):
                finalMatrixValue.append([])
                for column in range(self.columns):
                    finalMatrixValue[row].append(0)
            
            finalMatrix = Matrix(finalMatrixValue)

            for i in range(self.rows):
                for j in range(self.columns):
                    finalMatrix[i][j] = self[i][j] - other[i][j]
            
            return finalMatrix

    def __mul__(self, other):
        finalMatrixValue = []
        #The following code is to prevent pythons weird behaviour with lists created using k*[[a, b, c]] where editing one sublist will edit all others.
        if isinstance(other, (int, float, Matrix)):
            for row in range(self.rows):
                finalMatrixValue.append([])
                for column in range(self.columns if isinstance(other, (int, float)) else other.columns):
                    finalMatrixValue[row].append(0)
            finalMatrix = Matrix(finalMatrixValue)

        elif isinstance(other, Vector):
            if len(other) != self.columns:
                raise ValueError("Matrix must have as many columns as a vector has components to multiply.")
            finalVector = Vector([0 for _ in range(self.rows)])
        
        if isinstance(other, Matrix):
            if not (self.columns == other.rows):
                raise ValueError("Matrix dimensions do not match.")

            for i in range(self.rows):
                for k in range(other.columns):
                    #Location of value has been found, calculating value uses "Σ" so add another "for" loop
                    for j in range(self.columns):
                        finalMatrix[i][k] += self[i][j] * other[j][k]
            
        elif isinstance(other, (int, float)):
            for i, row in enumerate(self.values):
                for j, value in enumerate(row):
                    finalMatrix[i][j] = value * other
        
        elif isinstance(other, Vector):
            for i, row in enumerate(self.values):
                for j, value in enumerate(row):
                    finalVector[i] += value * other[j]
            return finalVector

        return finalMatrix

    def __rmul__(self, other):
        return self * other
    
    def __pow__(self, other):
        if isinstance(other, int):
            if self.rows != self.columns:
                raise ValueError("A matrix needs to be quadratic to be raised to an exponent.")
            finalMatrix = self
            for _ in range(other-1): # Subtract one from exponent as the power to one has already been made by setting finalMatrix = self
                finalMatrix *= self
        return finalMatrix

    def transpose(self):
        finalMatrixValue = []
        for i in range(self.columns):
            finalMatrixValue.append([])
            for j in range(self.rows):
                finalMatrixValue[i].append(self.values[j][i])
        
        return Matrix(finalMatrixValue)

    @functools.cache
    def determinant(self):
        """Calculate determinant using Laplace Expansion."""
        global factorList
        totalValue = 0
        if self.rows != self.columns:
            raise ValueError("Can only calculate determinants of quadratic matrices.")

        if self.rows == 2:
            totalValue = self[0][0] * self[1][1] - self[0][1] * self[1][0]

        else:
            for i in range(self.rows):
                if self.values[i][0] == 0:
                    continue
                otherMatrix = Matrix([[]])
                for a, row in enumerate(self.values):
                    if a == i:
                        continue
                    otherMatrix.values.append(row[1:])
                del otherMatrix.values[0]
                # In this case, we are forced to set the parameters "rows", "columns" of otherMatrix again as they are no longer accurate with these changes.
                otherMatrix.rows = len(otherMatrix.values)
                otherMatrix.columns = len(otherMatrix.values[0])

                # (-1)**i is added to make this calculation toggle between adding and subtracting, as is required in the Laplace Expansion.
                totalValue += factorList[(i+1)%2] * self.values[i][0] * otherMatrix.determinant()
        
        return totalValue
    
    
    def nonCacheDeterminant(self):
        """Calculate determinant using Laplace Expansion."""
        global factorList
        totalValue = 0
        if self.rows != self.columns:
            raise ValueError("Can only calculate determinants of quadratic matrices.")

        if self.rows == 2:
            totalValue = self[0][0] * self[1][1] - self[0][1] * self[1][0]

        else:
            for i in range(self.rows):
                if self.values[i][0] == 0:
                    continue
                otherMatrix = Matrix([[]])
                for a, row in enumerate(self.values):
                    if a == i:
                        continue
                    otherMatrix.values.append(row[1:])
                del otherMatrix.values[0]
                # In this case, we are forced to set the parameters "rows", "columns" of otherMatrix again as they are no longer accurate with these changes.
                otherMatrix.rows = len(otherMatrix.values)
                otherMatrix.columns = len(otherMatrix.values[0])

                # (-1)**i is added to make this calculation toggle between adding and subtracting, as is required in the Laplace Expansion.
                totalValue += factorList[(i+1)%2] * self.values[i][0] * otherMatrix.determinant()
        
        return totalValue


@functools.cache
def determinant(matrix: Matrix):
    """Calculate determinant using Laplace Expansion."""
    global factorList
    totalValue = 0
    if matrix.rows != matrix.columns:
        raise ValueError("Can only calculate determinants of quadratic matrices.")

    if matrix.rows == 2:
        totalValue = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    else:
        for i in range(matrix.rows):
            if matrix.values[i][0] == 0:
                continue
            otherMatrix = Matrix([[]])
            for a, row in enumerate(matrix.values):
                if a == i:
                    continue
                otherMatrix.values.append(row[1:])
            del otherMatrix.values[0]
            # In this case, we are forced to set the parameters "rows", "columns" of otherMatrix again as they are no longer accurate with these changes.
            otherMatrix.rows = len(otherMatrix.values)
            otherMatrix.columns = len(otherMatrix.values[0])

            # (-1)**i is added to make this calculation toggle between adding and subtracting, as is required in the Laplace Expansion.
            totalValue += factorList[(i+1)%2] * matrix.values[i][0] * determinant(otherMatrix)
        
    return totalValue


factorList = [-1, 1] # Predefining all possible factors for laplace expansion to avoid unnecessary calculations.
