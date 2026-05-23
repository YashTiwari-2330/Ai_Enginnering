num = int(input("Enter a number :-"))
orignal = num
rev = 0

while num > 0:
    rev = (rev * 10) + num % 10
    num = num // 10

if orignal == rev:
    print(f"{orignal} is palindrome")

else:
    print(F"{orignal} is not palindrome")