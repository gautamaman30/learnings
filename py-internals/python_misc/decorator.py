# Without arguement

def decorator(function):
    def wrapper(*args, **kwargs):
        function(args)
        print(args[0])
    return wrapper

@decorator
def say_hello_1(temp):
    print('1')
    print('Hello')

say_hello_1('Aman')


def add_name(name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            function(args[0])
            print(name)
        return wrapper
    return decorator

@add_name('Aman')
def say_hello_2(temp):
    print(2)
    print('Hello')

say_hello_2()