class Solution:
    def isPalindrome(self, x):
        return str(x) == str(x)[::-1]    
    
if __name__ == "__main__":
    import sys
    num = int(sys.stdin.read().strip())
    print(Solution().isPalindrome(num))
