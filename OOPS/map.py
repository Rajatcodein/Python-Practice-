print('Square of number ...',list(map(lambda x:x **2,[1,2,3,4,5,6,7])))

print('cube of number ...',list(map(lambda x:x **3,[1,2,3,4,5,6,7])))

print(list(map(lambda x:'even' if x%2==0  else 'odd',[1,2,3,4,5,6,7,8,9])))

print(list(map(lambda x: 'prime' if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1)) else 'not prime', [1, 2, 3, 4, 5, 6, 7, 8, 9])))

