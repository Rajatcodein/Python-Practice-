class Person:
    def __init__(self,name,gender):
        self.name = name
        self.gender = gender
        
p1 = Person('Rajat','male')
p2 = Person('dhananjay','male')
p3 = Person('faiz','male')

L  =[p1,p2,p3]
for i in L:
    print('collection of object using list',i.name,i.gender)
    
    print()
    
d ={'p1':p1,'p2':p2,'p3':p3}

for i in d:
    print('collection of object using dictionary',d[i].name,d[i].gender)