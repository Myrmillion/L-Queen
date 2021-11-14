# ---------------------
# IMPORTS
# ---------------------

from mpi4py import MPI


import time
import math
import numpy

# ---------------------
# GLOBAL VARIABLES
# ---------------------

result = []

# ---------------------
# UTILITY FUNCTIONS
# ---------------------


def isSafe(board, row, col):
    '''
    A utility function to check if a queen can be placed on board[row][col].
    Note that this function is called when "col" queens are already placed in columns from 0 to col -1.
    So we need to check only left side for attacking queens.
    '''

    n = len(board)

    # Check this row on left side
    for i in range(col):
        if (board[row][i]):
            return False

    # Check upper diagonal on left side
    i = row
    j = col
    while i >= 0 and j >= 0:
        if(board[i][j]):
            return False
        i -= 1
        j -= 1

    # Check lower diagonal on left side
    i = row
    j = col
    while j >= 0 and i < n:
        if(board[i][j]):
            return False
        i = i + 1
        j = j - 1

    return True


def solveNQUtil(result, board, col = 0, my_indices = ""):
    '''
    A recursive utility function to solve N Queen problem.
    '''

    # base case: If all queens are placed then return true

    n = len(board)

    if (col == n):
        v = []
        for i in board:
            for j in range(len(i)):
                if i[j] == 1:
                    v.append(j+1)
        result.append(v)
        return True

    # Consider this column and try placing this queen in all rows one by one

    res = False

    rows = []

    if col == 0:
        rows = my_indices
    else:
        rows = range(n)

    for i in rows:

        # Check if queen can be placed on board[i][col]
        if (isSafe(board, i, col)):

            # Place this queen in board[i][col]
            board[i][col] = 1

            # Make result true if any placement is possible
            res = solveNQUtil(result, board, col + 1) or res

            # If placing queen in board[i][col] doesn't lead to a solution, then remove queen from board[i][col]
            board[i][col] = 0  # BACKTRACK

    # If queen can not be place in any row in this column col then return false
    return res

def division_as_equal_groups(n, m):
    '''
    Divide `N` items into `M` groups with as near equal size as possible.
    
    We use the fact that : `N` = `N // M` * (M - (N % M)) + `(N // M) + 1` * (N % M).  
    So `N // M` -> number of groups with a `size = M - (N % M)`.
    And `(N // M) + 1` -> number of groups with a `size = N % M`.
    
    return `size 1, nb of groups with size 1), (size 2, nb of groups with size 2`.
    '''
    
    size_1 = n // m
    nb_groups_size_1 = m - (n % m)
    
    size_2 = (n // m) + 1
    nb_groups_size_2 = n % m
    
    return (size_1, nb_groups_size_1, size_2, nb_groups_size_2)
    

# ---------------------
# SOLVE FUNCTION
# ---------------------


def solveNQ(board, my_indices):
    '''
    This function solves the N Queen problem using Backtracking.
    It mainly uses solveNQUtil() to solve the problem.
    It returns false if queens cannot be placed, otherwise return true and prints placement of queens in the form of 1s.
    Please note that there may be more than one solutions, this function prints one of the feasible solutions.
    '''

    result = []

    solveNQUtil(result, board, 0, my_indices)

    return result


# ---------------------
# MAIN
# ---------------------

def main(N_SIZE):

    board = [[0 for _ in range(N_SIZE)] for _ in range(N_SIZE)]

    comm = MPI.COMM_WORLD
    my_rank = comm.Get_rank()
    nb_cores = comm.Get_size()

    # ----------- | START TIMER | ----------- #

    start = time.time()

    cores_indices = []
    
    if my_rank == 0:
        
        nb_tiles_1, nb_cores_1, nb_tiles_2, nb_cores_2 = division_as_equal_groups(N_SIZE, nb_cores)  
        current_indice = 0
        
        for _ in range(nb_cores_1):        
            cores_indices.append([i for i in range(current_indice, current_indice + nb_tiles_1)])
            current_indice += nb_tiles_1
                
        for _ in range(nb_cores_2):   
            cores_indices.append([i for i in range(current_indice, current_indice + nb_tiles_2)])
            current_indice += nb_tiles_2
    
    my_indices = comm.scatter(cores_indices, 0) # core 0 is the one scattering to others.
    result = solveNQ(board, my_indices)
    patterns = comm.gather(result, 0) # core 0 is the one gathering from others.

    end = time.time()

    # ----------- | END TIMER | ----------- #

    cores_times = comm.gather(end - start, 0)

    if my_rank == 0:
        
        final_result = []
        [final_result.extend(tab) for tab in patterns]
        
        #print(f"\n{final_result}")
        print(f"len = {len(final_result)}")
        print(f"\nWas executed in : {round(max(cores_times), 6)} seconds.")


if __name__ == "__main__":

    N_SIZE = 16

    main(N_SIZE)