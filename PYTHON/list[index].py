row1= ['1','2','3']
row2= ['4','5','6']
row3= ['7','8','9']

matrix=[row1,row2,row3]
print(f"{row1}\n{row2}\n{row3}")

position= input("enter a postion you want to make cross:")

row_num=int(position[0])
col_num=int(position[1])

row_select=matrix[row_num-1]
row_select=[col_num-1]='0'

print(f"{row1}\n{row2}\n{row3}")
