number=[1,2,2,3,3,3,2,4,4,5,4,6,4,4,6,5,4]
def most_freq(lst):
    max_count = 0
    most_time = None
    for item in lst:
        count = lst.count(item)
        if count > max_count:
            max_count = count
            most_time= item
    return most_time
print("most frequent element are",most_freq(number))