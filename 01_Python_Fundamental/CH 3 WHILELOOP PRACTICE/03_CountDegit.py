num = int(input("Enter Number :-"))
count = 0

while num > 0:
    num //= 10
    count += 1

    print("Number of digit is :-" , count)