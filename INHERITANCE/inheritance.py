# parents
class User :
    
    def __init__(self):
        self.name = 'rajat'
        self.gender = 'male'
        
    def Login(self):
        print('login')
 # child        
class Student(User):
    
    # def __init__(self):
    #     self.rollno = 121 
    
    # method OVERIDING 
    # AGAR  parent class ka constructor call nhi hoga to name print hoga hi nhi ...
    # so child class se constructor call nhi karenge so it will call by child class 
    
    # program flow kya hai phle child class call ho rha hai if constructor call hoga child class mein to parent class
    # ka constructor callhi nhi hoga 
    # so hmm child class me constrctor call nhi karenge !!!!
    
        
    def enroll(self):
        print(' enroll into a course ')
        
u = User()
s = Student()
print(s.name,s.gender)
s.enroll()
s.Login()

    