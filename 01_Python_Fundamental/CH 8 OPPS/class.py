class BankAccount:
    details = {}
    def __init__(self , acc_name , acc_number , balance=0 ):
        self.name = acc_name
        self.number = acc_number
        self.balance = balance

    def create_account(self):
            
            if not isinstance(self.name, str):
                raise ValueError("Name must be string")
            
            if not isinstance(self.number , int):
                raise ValueError("Number must be numaric")
            
            BankAccount.details[self.number] = self
            print("Account Created succesfully..")

       

acc = BankAccount("Yash" , 25874169)
acc.create_account()
print(BankAccount.details)
        