#!/usr/bin/env python3

'''
We wish to compute the total amount of water that will be held by some
topography when an infinite amount of evenly-distributed water is poured
on it from above. The topography is represented by a sequence of integers
describing the height of each unit-width section of terrain, from left to
right. Your solution will return the total amount of width-times-height
retained by the terrain. You may assume that heights are non-negative integers.

Solution by bt3gl
'''


def maxWater(arr) -> int:
    """
        Return the maximum water that can be stored
        Input: arr (an array of positive integers)
        Output: res (a positive integer)
    """

    res = 0
    n = len(arr)

    for i in range(n):

        # Define wall here
        left_wall = arr[i]
        right_wall = arr[i]

        # Find tallest walls
        for j in range(i):
            if left_wall < arr[j]:
                left_wall = arr[j]

        for j in range(i + 1, n):
            if right_wall < arr[j]:
                right_wall = arr[j]

        # Find shortest between tallest walls to get how much is
        # held and remove blocks in the middle from the some
        if right_wall < left_wall:
            res += right_wall - arr[i]
        else:
            res += left_wall - arr[i]

    return res



# Test 1
arr1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(f'Solution for {arr1} is {maxWater(arr1)} (and should be 6)')

# Test 2
arr2 = [2, 0, 2]
print(f'Solution for {arr2} is {maxWater(arr2)} (and should be 2)')

# Test 3
arr3 = [3, 0, 2, 0, 4]
print(f'Solution for {arr3} is {maxWater(arr3)} (and should be 7)')

# Test 4
arr4 = [0, 0, 0, 0]
print(f'Solution for {arr4} is {maxWater(arr4)} (and should be 0)')

# Test 5
arr5 = [5, 5, 5]
print(f'Solution for {arr5} is {maxWater(arr5)} (and should be 0)')