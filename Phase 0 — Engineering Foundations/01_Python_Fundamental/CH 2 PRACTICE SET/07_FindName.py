name = str(input("Enter Prompt :-" ))
find = str(input("Enter name's length :-"))

if(find in name):
    if(len(name) > 6):
        print(name , "Out of bound")
    print(find , " is talking about you")

else:
    print("They don't talk about you")