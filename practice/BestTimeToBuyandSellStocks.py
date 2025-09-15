"""""Problem Statement
Given an array prices where prices[i] is the price of stock on day i, find the maximum profit from one buy-sell transaction. You must buy before you sell.

Sample Input/Output
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy at price 1 (day 1), sell at price 6 (day 4) = profit 5

Input: prices = [7,6,4,3,1]  
Output: 0
Explanation: Prices only decrease, no profit possible"""

prices = list(map(int, input().split()))

min_price = prices[0]
max_profit = 0

for price in prices:
    min_price = min(min_price, price)
    profit = price - min_price
    max_profit = max(max_profit, profit)
print(max_profit)