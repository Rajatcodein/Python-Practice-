
 # if method name are same in both parent and child class so alway print child class method 
class phone:
    def __init__(self,price,brand,camera):
        print('Inside the phone constructor')
        self.price = price
        self.brand = brand
        self.camera = camera
       
    def buy(self):
        print('buying a phone')
        
class smartphone(phone):
    def buy(self):
        print('Buying a smartphone...')
        
s = smartphone(89000,'samsung',16)
s.buy()