# Decorators is a function that takes another function as a argument and return a function

def decorators(func):

    def wrapper():
        print("Decorator function started")
        func()
        print("Decorator functionended")

    return wrapper

@decorators
def hello():
    print("Execute decorator function")

hello()


def decorators_name(func):
    def wrapper(*args , **kwargs):
        print("Swap function started")
        print()
        func(*args , **kwargs)
        print()
        print("Swap function ended")

    return wrapper

@decorators_name
def swap(a ,b):
    print("Befor swapping a = {} and b = {}".format(a , b))
    a , b = b , a
    print("After swapping a = {} and b = {} ".format(a , b))

swap(10 , 20)