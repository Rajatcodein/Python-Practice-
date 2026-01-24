def HCFGCD(x,y):
    if x>y:
        smaller=y
    else:
        smaller =x
        hcf=1
    for i in range (1,smaller+1):
        if (x%i==0) and (y%i==0):
                hcf=i
    return hcf
print(" the hcf of both number is",HCFGCD(24,30))
    #  try:
    #     x = int(input("Enter the first number (x): "))
    #     y = int(input("Enter the second number (y): "))
    
    # # 2. Call the function with the user's input
    # result_hcf = HCFGCD(x, y)
    
    # # 3. Print the result
    # print(f"\nThe HCF/GCD of {x} and {y} is: {result_hcf}")

    # except ValueError:
    # print("Invalid input. Please enter valid integers.")