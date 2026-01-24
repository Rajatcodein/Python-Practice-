class testwala:
    def __init__(self,name,salary):
        self.name = name
        self.salary = salary
        
    def diaplay(self):
        print(self)
        print(self.name)
        print(self.salary)
a = testwala("anc","6789")
b = testwala("dfghj","676890")
a.diaplay()
b.diaplay()
        