"""
Problem Statement
Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct (unique).

Sample Input/Output

Example 1:
Input: nums = [1,2,3,1]
Output: true
Explanation: The element 1 occurs at indices 0 and 3

Example 2:
Input: nums = [1,2,3,4]
Output: false  
Explanation: All elements are distinct
"""
nums= list(map(int, input().split()))

seen = set()

for num in nums:
    if num in seen:
        print("Duplicate found")
        break
    seen.add(num)
else:
    print("No duplicates")    

