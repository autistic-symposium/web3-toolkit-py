#!/usr/bin/env python3
import sys


def _find_left_boundary(glob):
    """ 
        Given a glob, search for left boundary, returning a tuple with
        boundary values or None if boundary was not found. 
    """
    row, ncells = 0, 0

    while row < len(glob):
        col = 0
        
        while col < len(glob[row]):
            ncells = ncells + 1
            if glob[row][col] == 1:
                return (row, col), ncells
            else:
                col = col + 1
        row = row + 1        

    return None, ncells


def _find_right_boundary(glob):
    """ 
        Given a glob, search for right boundary, returning a tuple with
        boundary values or None if boundary was not found. 
    """
    row, ncells = len(glob) - 1, 0

    while row > 0:
        col = len(glob[row]) - 1
        
        while col > 0:
            ncells = ncells + 1
            if glob[row][col] == 1:
                return (row, col), ncells
            else:
                col = col - 1

        row = row - 1      

    return None, ncells
    

def _print_results(n_cells, top_left, bottom_right):
    """ 
        Print results in the desired format. 
    """
    print("Cell Reads : {}".format(n_cells)) 
    print("Boundary:") 
    print("     Top Left: {}".format(top_left)) 
    print("     Bottom Right: {}".format(bottom_right)) 


def main(glob):
    """ 
        Grab a NxN glob and print out the results. 
    """
    print("\nTesting {}".format(glob))

    if len(glob[0]) != len(glob):
        print("Matrix needs to be NxN.")
    
    else:
        top_left, nleft = _find_left_boundary(glob)
        if top_left:
            bottom_right, nright = _find_right_boundary(glob)
            if not bottom_right:
                bottom_right = top_left

            _print_results(nleft + nright, top_left, bottom_right)

        else:
            print("Could not find left boundary, maybe there is no 1s in your glob?")

        
if __name__ == "__main__":

    globs = []

    globs.append([[0, 1]])
    globs.append([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0], 
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0], 
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0], 
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    globs.append([[0, 0], [0,0]])
    globs.append([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    globs.append([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
    globs.append([[0, 1, 1], [0, 1, 1], [0, 0, 0]])

    for glob in globs:
        main(glob)

            