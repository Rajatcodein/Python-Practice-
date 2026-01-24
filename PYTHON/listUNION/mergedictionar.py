data ={'a':1,'b':2,'c':3,'d':4,'e':1}
data1 ={'a':1,'b':22,'c':3,'d':49,'e':1}

def merge_dict(data,data1):
    result = data.copy()
    for key , value in data1.items():
        if key in result:
            result[key] +=value
        else:
            result[key]=value
    return result
print(merge_dict(data,data1))