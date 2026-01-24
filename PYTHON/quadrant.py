import cmath
a=int(input(" enter a number(a != 0)"))
b=int(input(" enter a number"))
c=int(input("enter a number"))

d= (b**a) -(4*a*c)
root1 = (-b-cmath.sqrt(d))/(2*a)
root2 = (-b+cmath.sqrt(d))/(2*a)
print (root1,root2)