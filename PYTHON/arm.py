upper=int(input("enter a a upper limit "))

for num in range (1,upper+1):
    order=len(str(num))
    s=0
    t=num
    while t>0:
        digit=t%10
        cube=digit**order
        s = s + cube
        t//+10
if num==s:
    print(num," it is armstrong number")
else:
    print(" it is not armstrong number")