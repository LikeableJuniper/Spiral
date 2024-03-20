#################################################################
# This program was created to solve the problem depicted in problem.png.
# The goal is to calculate the coordinates of point A if the length of each segment is a gemoetrical series with q = 2/3 and a_1 = 39.
# Me and another pupil tried solving this problem using linear maps with 2x2 matrices but did not succeed, as the vectors cannot be represented as linear maps of each other.
# Our next thought was to expand this problem to 4 dimensions, using a 12x12 matrix and vector, where the first four components of the vector would result in two-dimensional x when added and the other four in two-dimensional y.
# The last four would be used to calculate the growth of the path length so one could subtract it from coordinates where needed.
# This would allow for more intricate manipulation of the coordinates with each iteration and might lead to a solution where using matrices could be viable.
#################################################################

from matrices import Matrix
from vectors import Vector

v = Vector(39, 0, 0, 0, 0, 0, 0, 0, 26, 0, 0, 0)
A = Matrix([
    # All x rows
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # All y rows
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    # Next increment
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/3],
    [0, 0, 0, 0, 0, 0, 0, 0, 2/3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2/3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2/3, 0],
])

print(A**6*v)
