data ={'a':1,'b':2,'c':3,'d':4,'e':1}
def most_freq(dict):
    frequency={}
    for value in dict.values():
        if value not in frequency:
            frequency[value]=0
        frequency[value]+=1  ##1:1,2:1,3:1,4:1,1:2
    max_value= max(frequency,key= frequency.get)
    return max_value
print(most_freq(data))