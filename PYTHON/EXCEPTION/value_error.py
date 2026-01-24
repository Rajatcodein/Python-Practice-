try:
    num = int(input("enter a number"))
    a= [6,25]
    print(a[num])
except ValueError:
    print("Number enter is not integer")
except ImportError:
    print("Index error")