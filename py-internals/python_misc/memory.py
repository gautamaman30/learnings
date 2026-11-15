# Python evaluates default arguments only once and mutable objects apply changes to same object that is why second_list is [2, 2]
def update(num = 2, my_list = []):
    print('Num id ', id(num))
    num += 2
    print('My list id ', id(my_list))
    my_list.append(2)    
    return num, my_list

first_num, first_list = update()
print('First num id ', id(first_num))
print(first_num)
print('First list id ', id(first_list))
print(first_list)

second_num, second_list = update()
print('Second num id ', id(second_num))
print(second_num)
print('Second list id ', id(second_list))
print(second_list)


# sum operator on list creates new ref as it evaluates right side first
# but in augment assignment python calls list.__iadd__(self, ...) method which has self and it adds to self
def list_sum():
    x = [1, 2]
    y = x 
    print('x and y ref the same object', x == y)
    x = x + [3, 4]
    print('x', x)
    print('y', y)
    print('x and y ref the same object', x == y)

    print('Reset')
    x = y 
    print('x and y ref the same object', x == y)
    x += [3, 4]
    print('x', x)
    print('y', y)
    print('x and y ref the same object', x == y)


list_sum()


# As tuples are immutable we cannot change the items (i.e. each item points to an obj and we cannot update that obj address in tuple)
# But if assign a list we can call list functions and change the list e.g append. As only list obj is updated and not the tuple.
t = 1, [1, 2]

try:
    t[1] = [1, 2, 3, 4]
except Exception as e:
    print('error', e)

t[1].append([3, 4])
print(t) 