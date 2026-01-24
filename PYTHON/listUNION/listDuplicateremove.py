fruits =["apple","banana","Guava","pineapple","watermelon","apple","banana","grapes","cheery","orange"]

def remove_duplicate(lst):
    unique =[]
    seen = set()
    for item in lst:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return unique
print(fruits)
print(" after removing duplicate item from list")
print(remove_duplicate(fruits))
print()
print("using set constructor we remove the duplicate list item from list ")

print(list(set(fruits)))    