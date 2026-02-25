def square (num):
    return num ** 2

print(type(square))
print(id(square))
s = square
print(s(3)) 


# storing in list 

L = [1,2,3,square]
print(' storing the function in list',L)
C = L [-1](3)
print(' calling function using list ',C)

# returning a functions 

def f():
    def x(a,b):
        return a+b
    return x
z =f()(3,5)
print('function return function ...->function f return function x that perform some operations',z)

# functions as arguement 
def func_a():
    print(' inside the function a')
def func_b(z):
    print(' inside the function b')
    return z()

print(func_b(func_a))