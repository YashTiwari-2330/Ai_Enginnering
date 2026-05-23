Math = int(input("Enter Math Marks :-"))
Science = int(input("Enter Science Marks :-"))
English = int(input("Enter English Number :-"))

Avg = (100*(Math + Science + English ))/300
print("Average is" , Avg)

if(Avg > 40):
    print("Student Pass")

elif(Avg >= 33 and Avg <= 40):
    print("Student * to pass")

else:
    print("Student Fail")