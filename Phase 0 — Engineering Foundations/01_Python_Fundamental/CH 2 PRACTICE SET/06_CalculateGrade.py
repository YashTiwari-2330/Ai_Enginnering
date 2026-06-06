import percentage

math = int(input("Enter Your Math marks :-"))
science = int(input("Enter Your Science marks :-"))
english = int(input("Enter Your English Marks :-"))
ss =  int(input("Enter Your SS marks :-"))

percentage = ((math + science + english + ss)*100)/400

if(percentage >= 90 and percentage <= 100):
    print(percentage , "Excellent")

elif(percentage >= 80 and percentage <= 90):
    print(percentage , "Grade A")

elif(percentage >= 70 and percentage <= 80):
    print(percentage , "Grade B")

elif(percentage >= 60 and percentage <=70):
    print(percentage , "Grade C")

elif(percentage >= 50 and percentage <= 60):
    print(percentage , "Grade D")

else:
    print(percentage , "Fail Try Next Time")