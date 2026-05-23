# Access a values of name

student = {
    "s1": 
    {"Name" : "Yash",
    "Age" : 22,
    "Gender" : "Male"},

    "s2" :
    {
        "Name" : "Akash",
        "Age"   : 20,
        "Gender" : "Male"
    }
}

print(student.get("Color" , "red"))

for id , details in student.items():
    print("Id :" , id)
    print("Name :" , details["Name"])
    print("Age :" , details["Age"])
    print()



cars = {
    "Car" : "BMW",
    "Model" : "xl6",
    "year" : 2022
}

count = 0

for car , model in cars.items():
    print(car , "->" , model)

for i in cars.keys():
    
    count += 1
print(count)


sums = {
    "a" : 10,
    "b" : 20,
    "c" : 30,
    "d" : 40,
}

for sum in sums.values():
    result = sum + sum

print(result)

uniq = dict(filter(lambda x : x[1] > 15 , sums.items()))
print(uniq)

max_rate = max(sums.values())

result = dict(filter(lambda x : x[1] == max_rate , sums.items()))
print(result)