import math

class Shape:
    def __init__(self , color="red"):
        self.color = color

    def area(self):
        return 0
    
    def __str__(self):
        return f"{self.__class__.__name__}(color={self.color})"
    
class Circle(Shape):
    def __init__(self, radius ,  color="red"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return round(math.pi * self.radius ** 2 , 2)
    
class Rectangle(Shape):
    def __init__(self, width , hight, color="red"):
        super().__init__(color)
        self.width = width
        self.hight = hight

    def area(self):
        return round(self.width * self.hight, 2)
    

c = Circle(5)
r = Rectangle(4,6)
s = Shape()

print(c.area())
print(r.area())
print(Shape().area())

print(c.color)
print(r.color)

c2 = Circle(3 , color="blue")
print(c2.color)
print(c2.area())