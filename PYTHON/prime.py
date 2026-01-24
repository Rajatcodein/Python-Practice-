n=int (input(" enter a number to check prime or not! "))
if n==1:
    print(" it is not  prime number")
if n>1:
    for i in range(2,n):
        if n%i==0:
            print(n," it is not prime number")
            break
    else:
        print(n,"it is prime number")
n1= int (input(" enter a upper limit num"))
for num in range (1,n1+1):
    if num>1:
        for i in range(2,num):
            if num%i==0:
                break
        else:
             print(num)
