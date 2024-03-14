#!/usr/bin/env python3

'''
We wish to compute the total amount of water that will be held by some
topography when an infinite amount of evenly-distributed water is poured
on it from above. The topography is represented by a sequence of integers
describing the height of each unit-width section of terrain, from left to
right. Your solution will return the total amount of width-times-height
retained by the terrain. You may assume that heights are non-negative integers.

Solution by Mia Stein
'''

def _create_wall_array(size) -> list:
    return [None for _ in range(size)]


def _get_tallest_wall(wall1, wall2) -> int:
    return (max(wall1, wall2))


def _get_water_filling(left_wall, right_wall, middle) -> int:
    return min(left_wall, right_wall) - middle


def maxWater(arr) -> int:
    """
        Return the maximum water that can be stored
        Input: arr (an array of positive integers)
        Output: res (a positive integer)
    """

    res = 0
    n = len(arr)
    left_wall = _create_wall_array(n)
    right_wall = _create_wall_array(n)
    left_wall[0], right_wall[n - 1] = arr[0], arr[n - 1]

    # Come from left
    for i in range(1, n):
        left_wall[i] = _get_tallest_wall(left_wall[i - 1], arr[i])

    # Come from right
    for i in range(n - 2, -1, -1):
        right_wall[i] = _get_tallest_wall(right_wall[i + 1], arr[i]);

    # Get water inside
    for i in range(n):
        res += _get_water_filling(left_wall[i], right_wall[i], arr[i])

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