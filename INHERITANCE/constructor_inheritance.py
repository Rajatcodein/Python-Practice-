class phone:
    def __init__(self,price,brand,camera):
        print('Inside the phone constructor')
        self.price = price
        self.brand = brand
        self.camera = camera
       
    def buy(self):
        print('buying a phone')
        
class smartphone(phone):
    pass

s = smartphone(90000,'samsung',13) 
s.buy()
    