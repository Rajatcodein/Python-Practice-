class Oops:
    def __init__(self):
        self.pin = ''
        self.balance = 0
        self.menu()
      # in python inside the class def is method 
      # outside the class functions  
    def menu (self):
        user_input = input(""" 
         Hi how can i help you
         1. press 1 to create pin 
         2. press 2 to change pin
         3. press 3 to check balance 
         4. press 4 to withdraw 
         5. Anything else to exit
         """)
        
        if user_input == '1':
           self.create_pin()
        elif user_input == '2':
            self.change_pin()
        elif user_input == '3':
            self.check_balance()
        elif user_input == '4':
            self.withdraw()
        else:
            exit()
            
    def create_pin(self):
            user_pin = input("enter a pin")
            self.pin = user_pin
            
            user_balance = int (input(" enter a balance"))
            self.balance = user_balance 
            
            print('pin created successfully') 
            self.menu()
            
    def change_pin(self):
        old_pin = input('enter old pin')
        
        if old_pin == self.pin:
            new_pin = input ('enter a new pin')
            self.pin = new_pin
            print(' pin change successfully')
            self.menu()
        else:
            print('nai change ho sakta bhai dekh le ')
            self.menu() 
            
    def check_balance(self):
        user_pin = input('enter a pin')
        if user_pin == self.pin:
            print(' Your balance is',self.balance)
        else:
            print('Please dekhle pin ko')
    
    def withdraw(self):
        user_pin = input('enter a pin')
        if user_pin == self.pin:
            amount= int(input('enter a amount..'))
            if amount < self.balance :
                self.balance= self.balance - amount
                print('withdraw sucessfully. balance is ',self.balance)
            else:
                print('insuficient balance ',self.balance)
        else:
            print('please dekh le bhai tera hi account hai .....')
                 
obj = Oops()
