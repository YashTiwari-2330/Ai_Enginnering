Somthing = str(input("Enter Message :-"))
spam = ("Make a lot of money ")
spam2 = ("Buy now")
spam3 = ("Subscribe this")
spam4 = ("Click this")


# "IN" KEYWORD ARE USE TO FIND A THING ARE EXIST IN YOUR PROGRAM OR NOT

if(Somthing in spam):
    print("This are a SPAM , Do not follow all the things blindly")

elif(spam2 in Somthing):
    print("This are a SPAM , Do not follow all the things blindly")

elif(spam3 in Somthing):
    print("This are a SPAM , Do not follow all the things blindly")

elif(spam4 in Somthing):
    print("This are a SPAM , Do not follow all the things blindly")

else:
    print(Somthing , " is Finding on my list")