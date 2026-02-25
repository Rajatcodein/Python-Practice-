class Parent:
    def __init__(self,num):
        self.__num = num
        
    def get_num(self):
        return self.__num
    
class child(Parent):
    def __init__(self,val,num):
        self.__val=val
        
    def get_val(self):
        return self.__val
    
son = child(100,12)
print('parent : num',son.get_num()) # run nhi hoga parent class k constructor call hi nhi hoga then it will not print parent num value it wil through a error 
print('child : val',son.get_val())
        