"""
Problem Statement
You can make multiple buy-sell transactions with these rules :
Buy and sell on any day
Only hold one share at a time (must sell before buying again)
Can buy and sell on the same day
Find maximum total profit

Sample Input/Output
Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: 
- Buy at 1, sell at 5: profit = 4
- Buy at 3, sell at 6: profit = 3  
- Total profit = 7

Example 2:
Input: prices = [1,2,3,4,5]  
Output: 4
Explanation: Buy at 1, sell at 5: profit = 4
(Or capture each daily increase: 1+1+1+1 = 4)"""

prices = list(map(int , input().split()))

total_profit = 0

for i in range(1, len(prices)):
    if prices[i] > prices[i-1]:
        total_profit += prices[i] - prices[i-1]
print(total_profit)
