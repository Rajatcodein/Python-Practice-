a=0
b=1
num = int(input(" enter sequence of fibonacci sequence.."))
if num==1:
    print(a)
else:
    for i in range(1,num):
        c=a+b
        a=b
        b=c
        print(c)