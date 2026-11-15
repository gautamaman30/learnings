# In generator we simply yield values and we don't need to implement __iter__ and __next__ like iterator. 
# With next() we manually iter through a generator or iterator instead of using for loop

# Fibonacci using generator
def fib(n):
    a, b = 0, 1
    while n > 0:
        a, b = b, a + b
        yield b
        n -= 1

temp = fib(7)
print('Fibonacci generator using next()')
print(next(temp))
print(next(temp))
print(next(temp))
print(next(temp))
print(next(temp))
print(next(temp))
print(next(temp))
try:
    print(next(temp)) # stop iteration error
except:
    print('Stop iteration error')

print('Fibonacci generator using for loop')
for i in fib(7):
    print(i)


# Fibonacci using iterator

class FibIterator:
    def __init__(self, max):
        self.max = max
        self.current = 0
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        self.current += 1
        return self.b
    
print('Fibonacci iterator using for loop')

fibIterator = FibIterator(7)
for i in fibIterator:
    print(i)

fibIterator = FibIterator(7)
print('Fibonacci iterator using next()')
print(next(fibIterator))
print(next(fibIterator))
print(next(fibIterator))
print(next(fibIterator))
print(next(fibIterator))
print(next(fibIterator))
print(next(fibIterator))
try:
    print(next(fibIterator)) # stop iteration error
except:
    print('Stop iteration error')