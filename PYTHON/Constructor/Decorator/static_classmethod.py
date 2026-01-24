class Student:
    grade = 5
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def get_data(self):
        print({'name' : self.name, 'age': self.age,'grade': self.grade})
        
    #using class method we can update the value of class variable like grade
    @classmethod
    def update_grade(cls,grade):
        cls.grade = grade
    
    @staticmethod
    def check_age(age):
        if age>18:
            print('Above 18')
        else:
            print('below 18')
    
    #  static method use without object 
s1 = Student('rajat',23)
s2 = Student('ram',33)

#s1.grade = 9
Student.update_grade(9)

Student.check_age(17)
s1.get_data()
s2.get_data()
