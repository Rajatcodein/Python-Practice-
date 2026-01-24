my_tuple =(1,2,3,4,2,4,45,60)
def find_index(tup,element):
    return tup.index(element) if element in tup else -1
a = int(input("Enter element u want to know the index positions "))
    
print(find_index(my_tuple,a))