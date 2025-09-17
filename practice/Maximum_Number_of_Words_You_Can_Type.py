class Solution:
    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        broken_set = set(brokenLetters)
        words = text.split()
        valid_word_count = 0
        for word in words:
            if not any(char in broken_set for char in word):
                valid_word_count += 1
        
        return valid_word_count
