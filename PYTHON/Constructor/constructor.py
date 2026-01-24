class A:
    dept = "Data Engineering"
    def __init__(self):
        name = "Rajat"
        print(name)
        # but if you print dept without self it give error so you refrence variable for particular class using self 
        print(self.dept)
obj = A()
