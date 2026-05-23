def login(username , password):
    c_username = "Yash"
    c_password = "yash2330"

    if username == c_username and password == c_password:
        return "Login successfully"
    
    elif username != c_username and password == c_password:
        return "Invlaid formate"
    
    elif username == c_username and password != c_password:
        return "Invalid formate"
    
    else:
        return "Invalid credantials"
    
username = input("Enter your username :- ")
password = input("Enter your password :- ")

print(login(username , password))

d_name = "Dmart System"

if login(username , password) == "Login successfully":
    print("Welcome to the Dmart captain")
    def calculate_total(quantity , price , tax = 0.5):
        total = quantity * price + tax
        return total

    name = input("Enter the name of the product :-")
    quantity = float(input("Enter the quentity :-"))
    price = float(input("Enter the price :- "))
    print(d_name)
    print(calculate_total(quantity , price))