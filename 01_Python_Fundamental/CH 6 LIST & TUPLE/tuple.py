# Single Element Tuple

tup = (1)

a = tup
print(type(a))

# UNpacke the value

unpacking = (10,20,30)

a , b , c = unpacking
print("Second value :- " , b)


# Swap the number 

a , b = 10,20
print(a , b)
a , b = b , a

print(a , b)


# Slicing

slic = (10,20,30,40,50,60)
print(slic[1:4])
print(slic[::-1])

lst = [10,20,50,70]
print(tuple(lst))

# Find max min

num = (1,5,7,8,2,4,6)
print(max(num))
print(min(num))
print()

# Check Element exixst

num = (10,20,40,50)
find = num.count(40)
if find == 0:
    print(f" number not exist")

else:
    print(f"found")


# Modify immutable tuple

number = ([10,20,30,50])
number.insert(3,40)
print(number)

# Nested Tuple access

num = (1,2,(3,4),(5,6))
print(num[2][0] , num[3][0])

# EXTEND UNPACKING

t = (1,2,3,4,5,6,7,8,9)
a = t[0]
b = t[-1]
rest = t[1:-1]
print(a , b , rest)