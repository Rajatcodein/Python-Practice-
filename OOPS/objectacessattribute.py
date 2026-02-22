class Person:
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def greet(self):

        if self.country == 'india' or 'INDIA':
            return f'Namaste, {self.name}'
        else:
            return f'Hello, {self.name}'

p = Person('rajat', 'IND')
print(p.name)
print(p.country)  # access atribute 
print(p.greet())  # access method 

# ATTRIBUTE CREATIONS FROM OUTSIDE OF CLASS 
p.gender = 'male'
print('ATTRIBUTE CREATIONS FROM OUTSIDE OF CLASS')
print(p.gender)