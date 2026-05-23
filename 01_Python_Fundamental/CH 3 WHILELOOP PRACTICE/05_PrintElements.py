num = int(input("Enter Number :-"))
j = 1

while j <= num:
    print([j*j])
    j += 1

print("Loop end")


# find x number in this tuple


sum = (1 ,4 , 9 ,16,25,36,49,64,81,100)

find = int(input("Enter Number Who find you :-"))
i = 0
while i < len(sum):
    if (find == sum[i]):
        print(f"Number of {find} Founded at index of {i}")
        break
    else:
        print(f"f{find} element does't exist in tuple")
    i+=1

