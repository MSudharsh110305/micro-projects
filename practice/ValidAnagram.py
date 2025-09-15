"""
Problem Statement
Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

Sample Input/Output
Example 1:
Input: s = "anagram", t = "nagaram"
Output: true
Explanation: Both contain same characters with same frequencies

Example 2:
Input: s = "rat", t = "car"
Output: false
Explanation: Different characters (no 't' in "car", no 'c' in "rat")
"""

string = input("Enter first string: ")
target = input("Enter second string: ")

from collections import Counter

if Counter(string) == Counter(target):
    print("Anagram")
else:
    print("Not an Anagram")
# Alternative approach without using Counter
# if sorted(string) == sorted(target):
#     print("Anagram")     
# else:
#     print("Not an Anagram")
# 