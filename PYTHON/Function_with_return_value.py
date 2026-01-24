# square of number of any number
def square(n):
    print(n**2)
square(5)

 
 
def square(n):  # parameter (placeholder)
    print(n**2)
result=square(7)
print(square(4)) # return None 
 

def square(n):
    return n**2
result=square(6)
print(result)


# funtion take 2 number as parameter 
def Sum(a,b):
    return a+b
a=int(input("enter a number"))
b=int(input("enter an number"))
result=Sum(a,b)
print (result)

# polymorphism
def Mul(a1,a2):
    return a1*a2
a1=int(input("enter a number"))
a2=int(input("enter a number"))
c=Mul(a1,a2)
print(c)
print(Mul(12,5))
print(Mul('RJ ',5))


# function return multiple values....
def circlestata(r):
  area =  3.14 *r**2
  cir= 2 *3.14 * r
  return area,cir
r=int(input("enter a number for geting circumfrence  and area :"))
a,c=circlestata(r)
print("circumference" ,c)
print("Area",a)
print(circlestata)


def greet(name="User"):
    return " hellow "+ name + " !!!!"
print(greet ("chaloo"))
print(greet())

# user input   .........
def greet(name):
    return " Hello " +name + "?...."
n=input('enter a name ')
p=greet(n)
print (p)

# lambfa function 
def cube(a):
    return a ** 3
a=int(input("enter an number "))
c=cube(a)
print (c)

cube = lambda X: X**3
print (cube(3))


# function with * argss
def sum_all(* args):
    return sum(args)
print (sum_all(1,2)) 
print(sum_all(1,3,4,2)) 

def sum_all(* args):
    print(*args)
    print(args)
    for i in args:
        print("Multiply of tuple value",i * 2)
    return sum(args)
print (sum_all(1,2)) 
print(sum_all(1,3,4,2))   

# **kwargs 
def kwargs(**kwargs):
    for key ,value in kwargs.items():
        print(f"{key}: {value}")
kwargs(Name=" RajaT ", Dept=" Data-Engg")
kwargs(Name="Python ",Dept="engginering",location="BLR")
kwargs(Name="Powerbi ")
kwargs(Name="sql ",Dept="engginer-mining",Salary=" Stipend",Profile=" Intern Data engg",reporting_mgr="souvik Das")

