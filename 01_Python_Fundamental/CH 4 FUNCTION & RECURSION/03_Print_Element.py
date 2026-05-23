cities = ["ahmedabad" , "Delhi" , "Rajkot" , "Bangalore"]

def print_len(list):
    for i in  list:
        print(i  , end=" " )

print_len(cities)


# FACTORIAL OF N

n = int(input("Enter Number :-"))

def factorial(n):
    fact =1
    for i in range(1 , n+1):
        fact *= i
    print(fact)

factorial(n)