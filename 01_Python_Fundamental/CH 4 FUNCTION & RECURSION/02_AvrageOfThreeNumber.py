# AVERAGE OF 3 NUMBER

num1 = int(input("Enter Number :-"))
num2 = int(input("Enter Number2 :-"))
num3 = int(input("Enter Number3 :-"))


def avg_number(num1 , num2 , num3):
    avg = 100 * (num1 + num2 + num3) / 300
    if avg == 0:
        print("0 Is not valid")
    print(avg)
    return avg


avg_number(num1 , num2 , num3)