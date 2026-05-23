# Dunder (double-underscore) methods let your class work with Python built-ins naturally. __str__ → print(), __len__ → len(), __eq__ → == operator, __add__ → + operator.

class Stack:
    def __init__(self):
        self._data = []

    def push(self , item):
        self._data.append(item)

    def pop(self):
        self._data.pop()

    def __len__(self):
        return len(self._data)
    
    def __str__(self):
        return f"Stack{self._data}"
    
    def __repr__(self):
        return f"Stack(size={len(self)})"
    
    def __bool__(self):
        return len(self._data) > 0
    
s = Stack()
s.push(10)
s.push(20)
s.push(30) 
s.pop()

print(len(s))
print(str(s))
print(repr(s))


class Vector:
    def __init__(self , x , y):
        self.x = x
        self.y = y

    def __add__(self):
        return self.x + self.y
    
    def __str__(self):
        return f"Stack({self.x , self.y})"
    
    def __eq__(self, value):
        return self.x == value or self.y == value
    
    def __len__(self):
        return len(self.x)


v = Vector(4 , 5)
print(f"Addition :- {v.__add__()}")
print(f"Display :- {v.__str__()}") 
print(f"Equal or not :- {v.__eq__(5)}")
print(f"Length :- {v.__len__()}")       
