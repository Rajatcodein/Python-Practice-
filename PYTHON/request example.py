import requests

x = requests.get('https://w3schools.com')
print("status code =",x.status_code)
print (x.text)
response = requests.get(x)

if response.status_code == 200:
        x = response.json()
        print(x.text)
