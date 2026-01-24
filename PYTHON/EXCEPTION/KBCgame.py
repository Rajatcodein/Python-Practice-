questions =[
[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

[" Which language was used by Data Enginnering ?","C","C++","Java","Python","None",4],

]

level =[1000,2000,3000,5000,10000,20000,40000,80000,160000,320000]
money =0
i =0
for i in range(0,len(questions)):
    question= questions[i]
    print(f"Question for Rs {level[i]}")
    print(f"a.{question[1]}    b.{question[2]}")
    print(f"a.{question[3]}    b.{question[4]}")
    reply= int(input("Enter a your answer(1-4) or 0 to quit"))
    if (reply==0):
        money=level[i-1]
        break
    if (reply == question[-1]):
        print(f"correct answer, you won Rs.{level[i]}")
        if(i==4):
            money=10000
        elif(i==9):
            money=320000
    else:
        print("wrong answer")
        break
print(f"you take home money is {money}")