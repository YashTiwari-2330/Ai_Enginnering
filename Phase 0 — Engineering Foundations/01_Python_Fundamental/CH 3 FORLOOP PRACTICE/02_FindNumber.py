num = [1,4,9,16,25,36,49,64,81,100]

x = int(input("Enter Found Number :-"))

for i in num:
    if i == x:
        print(f"{x} Founded")
        break
    else:
        print(f"{i}")

else:
    print("End")