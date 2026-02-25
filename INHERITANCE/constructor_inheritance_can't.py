class phone:
    def __init__(self,price,brand,camera):
        print('Inside the phone constructor')
        self.__price = price
        self.brand = brand
        self.camera = camera
       
    def show(self):
        print(self.__price)
        
class smartphone(phone):
    def check (self):
        print(self.price)
        
s=smartphone(20000,'samsung',13)
s.show()
