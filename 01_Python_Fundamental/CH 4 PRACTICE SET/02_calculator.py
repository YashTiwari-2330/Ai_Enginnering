def add(a , b):
    return a + b

def sub(a , b):
    return a - b

def mul(a , b):
    return a * b

def div(a , b):
    return a / b

print("Welcome To Calculator Application")
while True:
    choice = input("Enter choice (1-4) :- ")

    if choice == "1":
        num1 = float(input("Enter num1 :-"))
        num2 = float(input("Enter num2 :- "))
        print(f"{num1} + {num2} = {add(num1 , num2)}")

    
    elif choice == "2":
        num1 = float(input("Enter num1 :-"))
        num2 = float(input("Enter num2 :- "))
        print(f"{num1} + {num2} = {sub(num1 , num2)}")

    elif choice == "3":
        num1 = float(input("Enter num1 :-"))
        num2 = float(input("Enter num2 :- "))
        print(f"{num1} + {num2} = {mul(num1 , num2)}")

    elif choice == "4":
        num1 = float(input("Enter num1 :-"))
        num2 = float(input("Enter num2 :- "))
        print(f"{num1} + {num2} = {div(num1 , num2)}")

    else:
        print("Invalid Input")

        