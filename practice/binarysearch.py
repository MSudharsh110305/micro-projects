def binarysearch(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 5  
result = binarysearch(arr, target)
print(f"Element found at index: {result}" if result != -1 else "Element not found in array")
# Binary Search Implementation in Python
# Time Complexity: O(log n)
# Space Complexity: O(1)
