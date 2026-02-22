def mul (*args):
    product = 1 
    for i in args:
        product = product * i
    print(*args)   
    return product

print(mul(1,2,3,4,5,))
print(print.__doc__)
