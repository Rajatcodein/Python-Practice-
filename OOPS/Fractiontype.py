class fraction:
    def __init__(self,x,y):
        self.num = x
        self.deno = y
        
    def __str__(self):
        return '{}/{}'.format(self.num,self.deno)
    
    def __add__(self,other):
        new_num = self.num * other.deno + other.num * self.deno
        new_den = self.deno* other.deno
        
        return '{}/{}'.format(new_num,new_den)
fr1 = fraction(3,5)
fr2 = fraction(6,9)
print(fr1+fr2)