# Dictionary :-
             # Dictionary is an advance data type which provide a one to one relation betweeen key and values

# Create Dictionary

student = {
    "name" : "Yash",
    "age" : 21,
    "gender" : "Male"
}

# Access key
print(student.keys())

# Access values
print(student.values())

# Access both key and values
print(student.items())

# Loop

for key , value in student.items():
    print(key ,":" , value)


update = student["age"] = 22
print(student.items())

students = {
    "s1" : {"Name" : "Ajay" , "Age" : 22 , "Class" : 12},
    "s2" : {"Name" : "Aman" , "Age" : 22 , "Class" : 12}
}

print(students.values())
print(student.copy())