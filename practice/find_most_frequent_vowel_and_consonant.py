class Solution:
    def maxFreqSum(self, s: str) -> int:
        vowels = set('aeiouAEIOU')
    
        vowel_count = {}
        consonant_count = {}
        for char in s:
            if char.isalpha():
                if char in vowels:
                    vowel_count[char] = vowel_count.get(char, 0) + 1
                else:
                    consonant_count[char] = consonant_count.get(char, 0) + 1
        
        most_frequent_vowel = max(vowel_count.values(), default=0)
        most_frequent_consonant = max(consonant_count.values(), default=0)
        return most_frequent_vowel + most_frequent_consonant

# Example usage
solution = Solution()
result = solution.maxFreqSum("example sentence with vowels and consonants")
print(result)
