list=[1,2,3,4,5]
list1=[4,5,6,7,8,9,10]

def intersection_list(lst,lst1):
    common_list=[]
    for item in lst:
        if item in lst1 and item not in common_list:
            common_list.append(item)
    return common_list
print("The common element from both list are ",intersection_list(list,list1))

# using list compherension 
def intresection_comp(lst,lst1):
    return[item for item in lst if item in lst1]
print ("common element are using list comphernsion",(intresection_comp(list,list1)))