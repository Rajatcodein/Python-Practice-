num=[1,2,3,4,5,6,7,8,9]

def commulative_list(lst):
    cum_sum =[]
    t =0
    for item in lst:
        t += item
        cum_sum.append(t)
    return cum_sum
print("commulative sum of list",commulative_list(num))