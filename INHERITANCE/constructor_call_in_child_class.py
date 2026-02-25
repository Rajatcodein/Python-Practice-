class phone:
    def __init__(self,price,brand,camera):
        print('Inside the phone constructor')
        self.price = price
        self.brand = brand
        self.camera = camera
       
    def buy(self):
        print('buying a phone')
        
class smartphone(phone):
    def __init__(self, os,ram):
        self.os = os
        self.ram = ram
        print('Inside the smartphone constructor....')
        
    def buy(self):
        print('Buying a smartphone...')
        
s=smartphone('android',2)
s.buy()
#p=phone(20000,'samsung',13)