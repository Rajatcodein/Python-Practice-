def fac(n):
    f=1
    for i in range (n):
        f=f*(i+1)
    return f
n=int (input(" enter a number "))

print(fac(n) )