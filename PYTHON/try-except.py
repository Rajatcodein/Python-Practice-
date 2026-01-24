a= int (input("enter a number "))
b= int (input("enter a number "))
try:
    c=a/b
    print(" Resultant value is ",c)
except:
    print("can't divide by zero....")
else:
    print(" try -exception ")