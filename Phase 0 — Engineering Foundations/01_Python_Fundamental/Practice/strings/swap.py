from functools import wraps


def swap_logger(func):
    @wraps(func)
    def wrapper(self, a, b):
        print(f"Before swap: a = {a}, b = {b}")
        swapped_a, swapped_b = func(self, a, b)
        print(f"After swap: a = {swapped_a}, b = {swapped_b}")
        return swapped_a, swapped_b

    return wrapper


class Solution:
    @swap_logger
    def swap(self, a, b):
        a, b = b, a
        return a, b


a, b = 5, 15
print(Solution().swap(a, b))


# Reverse numbers

def reverse_number(num):
    reverse = str(num)[::-1]
    return int(reverse)

num = 123
print(f"Original number :- {num}")
print(f"Reversed number :- {reverse_number(num)}")


# Count Digit

def count_digit(num):
    count = 0
    while num > 0:
        num //= 10
        count += 1
    print(count)

num = 12345678910
print(f"Orignal number :- {num}")
print(f"Count of digits in {num} is :-")
count_digit(num)


# Check palindrome number

def check_palindrome(num):
    orignal = num
    reverse = str(num)[::-1]
    if orignal == int(reverse):
        return f"{orignal} is a palindrome number"
    
    else:
        return f"{orignal} is not a palindrome number"
    

num = 12321
print(check_palindrome(num))

# Find Factorial

def factorial(num):
    if num == 0 or num  == 1:
        return 1
    else:
        return num  * factorial(num - 1)
    
num = 5
print(f"Factorial of {num} is :- {factorial(num)}")



# Find GCD

def gcd(a,b):
    if a == 0:
        return b
    
    if b == 0:
        return a
    
    if a == b:
        return a
    
    if a > b:
        return gcd(a -b ,b)
    
    return gcd(a , b - a)

a = 25
b = 15
print(gcd(a , b))

# Check armstrong number

def check_armstrong(num):
    orignal = num
    sum = 0
    while num > 0:
        digit = num % 10
        sum += digit ** 3
        num //= 10

    if orignal == sum:
        return f"{orignal} is an armstrong number"
    
    else:
        return f"{orignal} is not an armstrong number"
    
num = 153
print(check_armstrong(num))

# Find all prime numbers in a range

def is_prime(num):
    if num <= 1:
        return "Not valid"
    
    for i in range(2 , num):
        if num % i == 0:
            return False
    return True

def prime_in_range(start , end):
    prime = []
    for num in range(start , end +1):
        if is_prime(num):
            prime.append(num)
    return prime
    
start = 2
end = 100

print(prime_in_range(start ,end))

# Implement power function without **

def power(base , exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result

base = 2
exp = 5
print(power(base , exp))

# Compute the nth Fibonacci number

def fibonacci(n):
    if n <= 0:
        return 0
    
    elif n == 1:
        return 1
    
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    
n = 10
print(f"The {n}th Fibonacci number is :- {fibonacci(n)}")



# Two sum

class Solution:

    def two_sum(self , num , target):
        new_dict = {}

        for i in enumerate(num):
            result = target - num[i]
            if result in new_dict:
                return [new_dict[result] , i[1]]
            new_dict[num[i]]= i[1]

num = [2,7,8,11,15]
target = 9
print(Solution().two_sum(num , target))
