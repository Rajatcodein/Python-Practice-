# import random ,itertools
# deck= list ( itertools.product (range((1,14)),[" spade","club"," daimond","heart"]))
# random.shuffle(deck)
# print(deck)
# for i in range(5):
#     print(deck[i][0]," of ",deck[i][1])
    
import random
import itertools
deck = list(itertools.product(range(1, 14), ["spade", "club", "diamond", "heart"]))
random.shuffle(deck)
print("Drawing the top 5 cards:")
for i in range(5):
    print(f"{deck[i][0]} of {deck[i][1]}")

