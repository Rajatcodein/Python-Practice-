def Square (x):
    return x**2

def cube (y):
    return y**3

def tranform(f,C,L):
    out =[]
    out1=[]
    for i in L:
        out.append(f(i))
        out1.append(C(i))
    print(out)
    print(out1)
L=[1,2,3,4,5,6,7]
print(tranform(Square,cube,L))

# USE OF HOF IN ANOTHER APPROACH.........
print('USE OF HOF IN ANOTHER APPROACH.........')
def Square (x):
    return x**2

def cube (x):
    return x**3

def tranform(f,L):
    out =[]
    for i in L:
        out.append(f(i))    
    print(out)
L=[1,2,3,4,5,6,7]
print(tranform(lambda x:x**2,L))
print(tranform(lambda x:x**3,L))