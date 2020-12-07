import math


class Solution:


    def generate_sqrt(self, num1):
        total = 0
        list_num = list(str(num1))
        for i in list_num:
            total += pow(int(i), 2)
        return total

    def isHappy(self,n):
        counter = 0
        while counter <= 100:
            counter += 1
            temp = self.generate_sqrt(n)
            if temp == 1:
                print(True)
                return True
            else:
                n = temp
        print(False)
        return False


#if __name__ == "__main__":
n = int(input())
test = Solution()
test.isHappy(n)


