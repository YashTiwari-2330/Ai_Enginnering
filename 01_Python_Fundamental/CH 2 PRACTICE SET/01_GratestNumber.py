num1 = int(input("Enter Number 1:-"))
num2 = int(input("Enter Number 2:-"))
num3 = int(input("Enter Number 3:-"))
num4 = int(input("Enter Number 4:-"))

if(num1 > num2 and num1 > num3 and num1 > num4):
    print("num 1 is big")

elif(num2 > num1 and num2 > num3 and num2 > num4):
    print("{Num2} is big")

elif(num3 > num4 and num3 > num1 and num3 > num1):
    print("Num3 is bigger")

else:
    print("Num4 is bigger")