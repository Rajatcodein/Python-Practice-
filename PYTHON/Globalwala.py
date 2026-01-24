l=23
def Fun(n):
    l=5
    m=4
    #global l
    l=l+5
    print(l, m)
    print(n,"l have do it ")

Fun("this ")
x=98000
def RJ ():
    global x
    x=60000
    def Rajat():
        global x
        x=720000
    print(" before calling Rajat()",x)
    Rajat()
    print("after calling Rajat()",x)
RJ()
print(x)