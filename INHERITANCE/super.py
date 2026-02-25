 # super keyword super() is a built-in function that allows a child class to call methods and access properties from its parent class
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
        # syntax for super that acess parent k buy method 
        super().buy()
s = smartphone(89000,'samsung',16)
s.buy()