class A:
    age = 23
    name = "RajaT Modanwal"  # member of class so we can acess using self which is act as refrence to acess name
    def __init__(self):
        print(self.name)
    def Show(self):  # its not cnstructor so we create obj to access it 
        print(self.age)
obj = A()
obj . Show()
