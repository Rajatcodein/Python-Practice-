person = { 'name': 'Rajat','dept': 'Data Engg','location':'Bangaluru'}

print(person)
print(type(person))

print(" method 2 using dict () constructor")

per1 = dict (name ='RJ',age ='23',qal= ' MCA')
print(per1)
print(type(per1))


print("----------- method 3 using list of tuples---------")

per2 = dict([('naam','Rajat'),('umar',23),('jagah','bangalore')])
print(per2)
print(type(per2))


print("------------ Accessing the item from dictionary--------")
print(per1['age'])

print(person['dept'])
print(per2['naam'])

print(person.keys())
print(person.items())
print(per1.values())


print(" Add Item in ------------")
person['email']= 'rajat.gupta@protium.co.in'
print(person)

for keys in person:
    print(keys)

for value in per2:
    print(per2[value])

for keys,value in person.items():
    print(keys,value)