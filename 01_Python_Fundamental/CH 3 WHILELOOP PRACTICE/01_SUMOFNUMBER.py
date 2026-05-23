number = int(input("Enter a number :-"))
total = 0
n = 1

while(n <= number):
    total += 1
    n+= 1

    print("sum", total)


print("Multiplication table program start..")
num = int(input("Enter Table Number :-"))
j = 1

while j <= 10:
    print(f"{num} * {j}  =  {num * j}" )
    j += 1