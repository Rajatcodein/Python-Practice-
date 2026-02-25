# refrence variable hold the object
# we can create object without refrence variable as well
# an object can have multiple refrence variable 
# assigning a new refrence variable to existing object does not create a new object

class Person:
    def __init__(self):
        self.name = 'rajat'
        self.gender = ' male'
        
p = Person()
q = p
print(id(p))
print(id(q))
print(p.name)
print(q.name)
q.name = 'rahul'
print(p.name)
print(q.name)
