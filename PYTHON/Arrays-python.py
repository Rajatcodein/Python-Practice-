import array as myarr
arr = myarr.array('i',[1,2,3])
arr1 = myarr.array('d',[1.0,2.0,3.3,4.6])
arr2 = myarr.array('u',['a','b','c','d'])

print(arr.typecode)
print(arr1.typecode)

print(arr2.typecode)

print(arr)
print(arr1)
print(arr2)

print(len(arr))
print(len(arr1))
print(len(arr2))

print(" using For loop how acesss element of array  ")
for i in range(0,len(arr)):
    print(arr[i],end=' ')
print("\n")
for i in range (0,len(arr1)):
    print(arr1[i],end=' ')
print("\n")
for i in range(0,len(arr2)):
    print(arr2[i],end=' ')
print("\n")

x=list(range(1,100,4))
new=myarr.array('i',x)

for i in range (0,len(new)):
    print(new[i],end=' ')
print("\n")
print(" using while loop ")
n=len(new)
i=0
while (i<n):
    print(new[i])
    i+=1

new1=myarr.array('i',[2,3,23,432,456,87654])
for i in range (0,len(new1)):
    print(new1[i],end=' ')
print("\n")

new1.insert(0,1)
new1.insert(0,0)

for i in range(0,len(new1)):
    print(new1[i],end=' ')
print("\n")

new1[2]=60
for i in range(0,len(new1)):
    print(new1[i],end=' ')
print("\n")

new1.pop()
for i in range (0,len(new1)):
    print(new1[i],end=' ')
print(" searching operation in arrray")

x=list(range(0,100000,))
search_arr= myarr.array('i',x)
for i in range (0,len(search_arr[0:10])):
    print(search_arr[i],end=' ')
print("\n")
index=search_arr.index(1009)
res=search_arr[index]
print(index,res)
print(" user input to take number of element in array and print the value ")
arr =myarr.array ('i',[])
n= int(input(" enter a length (size ) of array ...."))
for i in range (n):
    x=int(input(" enter a element of array"))
    print("\n")
    arr.append(x)

print(arr)

ser=int(input(" enter a element u want to search"))
j=0
for e in arr:
    if e==ser:
        print(j)
        break
    j+=1
else:
    print( ser,"  not present in arrays")

