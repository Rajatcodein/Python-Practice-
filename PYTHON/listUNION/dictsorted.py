data ={'a':150,'b':92,'c':103,'d':4,'e':11}
def sort_by_value(data):
    sorted_items= sorted(data.items(),key = lambda item : item[1])
    return{key:Value for key,Value in sorted_items}
print(sort_by_value(data))
    
