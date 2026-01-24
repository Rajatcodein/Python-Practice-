set0={30,65,150,'Data Eng',True,30,1}
# the above duplicate value are not print because true=1 
print(set0)
# indexing are not allowed
##    #print(set[2])
# EMPTY SET ALWAY DICT TYPE
set1={}
print(type(set0))
print("set1 type=",type(set1))

# if you want create empty set that have another ways
set2=set()
print("Empty set2 type = ",type(set2))

# SET are not allowed to assigened values 
#      set0[2]=200

# Using .add .remove method you can add the value or remove the value in set
set0.add(200)
print(" the updated set0 value = ",set0)
print(len(set0))

set0.discard(99)
print(set0)

# if we add list in set so its not add because list are mutable 
# ######     set0.add([12,23,32,2])
#####        print(set0)

