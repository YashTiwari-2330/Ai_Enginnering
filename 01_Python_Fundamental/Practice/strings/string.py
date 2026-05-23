# String are the collectuion of the multiple characters , 
# STring are imutable and ordered collection of the characters

# Validate the string project with cover all the following methods

# 1. String concatenation

str = "Hello"
str1 = "WORLD"

result = str.casefold().capitalize() + " " + str1.casefold().capitalize()
print(result)


text = "{subject} is doing {activity} at {time}"

result = text.format(subject = "Yash" , activity = "Coding" , time = "Night")
print(result)

str = "Hello World"

print(str.lstrip("Hello "))
print(str.rstrip(" world"))
print(str.strip("Hello World"))

print(str.rsplit(" " ))
print(str.split(maxsplit=0))


# 1. FizzBuzz
# Print 1–100. For multiples of 3 print "Fizz", for 5 print "Buzz", for both print "FizzBuzz".

for i in range(1 , 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")

    elif i % 3 == 0:
        print("Fizz")

    elif i % 5 == 0:
        print("Bizz")

    else:
        print(i)

# Reverse string without slicing using methods

def reverse_string(s):
    new_string = ""
    for i in s:
        new_string = i + new_string

    if new_string == s:
        return "Palindrome"
    
    return new_string

print(reverse_string("OyO"))
        

def count_vovels(s):
    count = 0
    for i in s:
        if i in "aeiouAEIOU":

            count += 1

    return count


print(count_vovels("Hello wrold"))



class Solution:
    def isPalindrome(self , s):
        new_string = ""
        for i in s:
            if i.isalnum():
                new_string += i.lower()

        if new_string == new_string[::-1]:
            return f"{new_string} is a palindrome"
        
        return f"{new_string} is not a palindrome"
    
s = "A man, a plan, a canal: Panama"
print(Solution().isPalindrome(s))