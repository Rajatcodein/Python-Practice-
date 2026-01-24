    
def fun():    
    try:
        l=[1,12,3,4,]
        i=int(input("enter a number"))
        print(l[i])
        return 1
    except:
        print("some error occured")
        return 0
    finally:
        print("I am always executed wheather try or except executed")
x = fun()
print(x)