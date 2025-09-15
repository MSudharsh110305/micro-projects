"""
Problem Statement
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

Assumptions:

    Each input has exactly one solution
    Cannot use the same element twice
    Can return the answer in any order

Sample Input/Output

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums + nums[9] == 9, return [0, 1]

Example 2:
Input: nums = [3,2,4], target = 6  
Output: [1,2]
Explanation: nums[9] + nums[10] == 6, return [1, 2]"""


nums = [2,7,11,15]
target = 9
num_to_index = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in num_to_index:
        print([num_to_index[complement], i])
    num_to_index[num] = i
