class fraction:
    def __init__(self,x,y):
        self.num = x
        self.deno = y
        
    def __str__(self):
        return '{}/{}'.format(self.num,self.deno)
    
print( fraction(4,8))


class fraction:
    def __init__(self, x, y):
        self.num = x
        self.deno = y

    def __str__(self):# magic method
        return f"{self.num}/{self.deno}"

# Capture user input and cast to integers
n = int(input("Enter numerator: "))
d = int(input("Enter denominator: "))

# Create and print the object
f = fraction(n, d)
print(f"Your fraction is: {f}")
