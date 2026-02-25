class Parent:
    def __init__(self,num):
        self.__num = num
        
    def get_num(self):
        return self.__num
    
class child(Parent):
    def show(self): #self is a placeholder that tells the code to use the specific object you just created
        print('This is in child class')
        
son = child(100)
print(son.get_num())
son.show()