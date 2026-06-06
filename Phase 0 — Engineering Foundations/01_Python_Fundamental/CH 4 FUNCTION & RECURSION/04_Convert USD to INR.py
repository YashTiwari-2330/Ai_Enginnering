# number = int(input("Enter Dollar :-"))
# dollar = 87.57
# def dolor_count(number):
#     number *= dollar
#     print("Dolor In Indian Rupeee" , number , "INR")
#
# dolor_count(number)
#
# #  FIND EVEN OR ODD USING FUNCTION
#
# num = int(input("Enter Number :-"))
#
# def type_number(num):
#     if num % 2 == 0:
#         print(f"{num} is Even")
#
#     else:
#         print(f"{num} is Odd")
#
# type_number(num)
#
# # FACTORIAL OF NUMBER
#
# fact = int(input("Enter Number :-"))
#
# def factorial(n):
#     if n == 1 or n == 0:
#         return 1
#     return n* factorial( n - 1)
#
# print(factorial(fact))
#
# # FIND MAXIMUM NUMBER
#
# a = int(input("Enter Number1 :-"))
# b = int(input("Enter Number2 :-"))
# c = int(input("Enter Number3 :-"))
#
# def find_max(a , b ,c):
#      return max(a , b ,c)
# print(find_max(a,b,c))

# CHECK PALINDROME OR NOT IN STRING

String = str(input("Enter String :-"))

def palindrome(str):
    if str == str[::-1]:
        return (f"{str} is a palindrome")
    else:
        return (f"{str} is not palindrome")
print(palindrome(String) )


# CHECK PALINDROME OR NOT IN NUMBER

num = int(input("Enter Number :-"))
orignal = num

def find_palindrome(i):
    rev = 0
    while i > 0:
        rev = (rev * 10) + i % 10
        i = i //10

    if orignal == rev:
        print(f"{orignal} is palindrome")

    else:
        print(f"{orignal} is not palindrome")

print(find_palindrome(num))
