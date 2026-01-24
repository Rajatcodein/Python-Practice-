a = input("Enter a number")
print(f"Multiplications of table {a} is")

try:
    for i in range (1,11):
        print(f"{int(a)}X {i}={int(a)*i}")
except Exception as e:
    print("Sorry Some error occured",e)