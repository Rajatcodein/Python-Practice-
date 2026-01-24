My_aim = "I want become data engineer"
def protium():
    job = "I am intern in data engineer dept"
    print(job)
protium()
print(My_aim)


def DataEngineer ():
    global current_salary_standard
    current_salary_standard=600000
    def Protium():
        global current_salary_standard
        print(current_salary_standard)
        current_salary_standard=720000
    print(" before joining protium()",current_salary_standard)
    Protium()
    print("after joining Protium()",current_salary_standard)
DataEngineer()
print(current_salary_standard)
