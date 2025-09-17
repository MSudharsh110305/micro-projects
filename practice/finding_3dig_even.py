from collections import Counter
from typing import List
class Solution:
    def findEvenNumbers(self, a: List[int]) -> List[int]:
        z = Counter(map(str,a))
        return [v for v in range(100,1000,2) if Counter(str(v))<=z]

# since only there are 900 three digit even numbers, we can just check each of them
# convert the number to string and use Counter to count the digits
# then check if the count of each digit is less than or equal to the count in the array
# if yes, add the number to the result list
