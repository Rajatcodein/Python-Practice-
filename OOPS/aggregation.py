class Customer:
    def __init__(self,name,gender,address):
        self.name = name
        self.gender = gender
        self.address = address
        
        
    def print_address(self):
        return(self.address.city,self.address.pin,self.address.state)
    
    def edit_profile(self,new_name,new_pin,new_city,new_state):
        self.name = new_name
        self.address.edit_profile_info(new_city,new_pin,new_state)
        
class Address:
    def __init__(self,city,pin,state):
        self.city = city
        self.pin = pin
        self.state = state
        
    def edit_profile_info(self,new_city,new_pin,new_state):
        self.city = new_city
        self.pin = new_pin
        self.state = new_state
        
add1 = Address('varanasi',221108,'UP')
cust = Customer('rajat','male',add1)
cust.print_address()
cust.edit_profile('rahul','BLR',56012,'KA')
cust.print_address()

print(cust.name,cust.print_address(),cust.gender)
        
    