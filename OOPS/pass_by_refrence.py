class Person:
    def __init__(self,name,gender):
        self.name = name
        self.gender = gender
        
    #   OUTSIDE CALL THE FUNCTIONS
def greet(person):
    print(' Hi my name is ',person.name,'and I am a',person.gender )
    
p = Person('Rajat','male')
greet(p)

print('------------------------------------------------')

class Person:
    def __init__(self,name,gender):
        self.name = name
        self.gender = gender
        
    #   OUTSIDE CALL THE FUNCTIONS
def greet(person):
    person.name = 'ram'
    return person
    
p = Person('Rajat','male')
print(id(p))
p1 = greet(p)
print(id(p))
print(p.name)
