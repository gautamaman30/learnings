class PersonSingleton:
    _instance = None
    _initialized = None

    def __new__(cls, *args, **kwargs):
        print('New method called')
        if cls._instance is None:
            cls._instance = super(PersonSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, name):
        if PersonSingleton._initialized:
            return
        PersonSingleton._initialized = True
        print('Init method called')
        self.name = name

    def say_hello(self):
        print('Hello ' + self.name)

# person_1 = PersonSingleton('Aman 1')
# person_1.say_hello()
# person_2 = PersonSingleton('Aman 2')
# person_2.say_hello()



class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    # def __mul__(self, other):
    #     return Vector2D(self.x * other.x, self.y * other.y)
    
    def __mul__(self, scaler):
        return Vector2D(self.x * scaler, self.y * scaler)
    
    def __rmul__(self, scaler):
        return Vector2D(self.x * scaler, self.y * scaler)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
    
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** (0.5)
    

v1 = Vector2D(3, 4)
# __str__ is called for string representation of the object
print(v1)

v2 = Vector2D(1, 2)

v3 = v1 + v2
print(v3)

v4 = v1 - v2
print(v4)

# v5 = v1 * v2
# print(v5)

v5 = v1 * 2
print(v5)

v6 = 3 * v1
print(v6)

print(v1 == v2)

print(-v1)

print(abs(v1))
