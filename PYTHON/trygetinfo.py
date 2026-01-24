import requests
import json

def fetch_powerbi_workspaces(access_token,workspaces):
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo"
    print("checked")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "workspaces": workspaces
    }

    response = requests.post(url, headers=headers,json=payload)
    print(response)
    
    if response.status_code == 200:
        workspaces = response.json()
        batch_size = 50  
        batches = batch_array(workspaces, batch_size)

       
        for i, batch in enumerate(batches):
            print(f"Batch {i + 1}:")
            print(json.dumps(batch, indent=4))
            # json.dumps()method can convert a Python object into a JSON string.
    else:
        print(f"Failed to fetch workspaces. Status code: {response.status_code}, Message: {response.text}")
        
def batch_array(data, batch_size):

    batch_size.append(data) 
   
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
    

def main():
    
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkhTMjNiN0RvN1RjYVUxUm9MSHdwSXEyNFZZZyIsImtpZCI6IkhTMjNiN0RvN1RjYVUxUm9MSHdwSXEyNFZZZyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNTc5NjBkM2UtNzdkYS00MDE3LTlkYmUtNGNiYjdkNmE3MTk0LyIsImlhdCI6MTc1OTkwMzUwMiwibmJmIjoxNzU5OTAzNTAyLCJleHAiOjE3NTk5MDc0MDIsImFpbyI6ImsySmdZSGh6d2ZDWjgyOTl4YnNIOWVKVkQ3U2VCQUE9IiwiYXBwaWQiOiJiZDhhNTdiNC1hNzU0LTRkNjktODZjYy1mMGNlM2UxNjRlNzkiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81Nzk2MGQzZS03N2RhLTQwMTctOWRiZS00Y2JiN2Q2YTcxOTQvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiJlYWQ1YjhkMC05MWE0LTRkODMtOTJkZS0wMjMxOWIzNjc3YWEiLCJyaCI6IjEuQVQ0QVBnMldWOXAzRjBDZHZreTdmV3B4bEFrQUFBQUFBQUFBd0FBQUFBQUFBQURIQUFBLUFBLiIsInN1YiI6ImVhZDViOGQwLTkxYTQtNGQ4My05MmRlLTAyMzE5YjM2NzdhYSIsInRpZCI6IjU3OTYwZDNlLTc3ZGEtNDAxNy05ZGJlLTRjYmI3ZDZhNzE5NCIsInV0aSI6ImR5MEUwZ3dBVWtDYU9KeWpPMnVQQUEiLCJ2ZXIiOiIxLjAiLCJ4bXNfZnRkIjoicGVhNFhWd21kcUIyc05kSjY0VFpOakRqVDE0aE9HTXFfUzhtSFFJQnV1RUJhbUZ3WVc1bFlYTjBMV1J6YlhNIiwieG1zX2lkcmVsIjoiNyAxMiIsInhtc19yZCI6IjAuNDJMbFlCSml0Qk1TNFdBWEV2aFd5UzM1SUVmUHVfVlY0dkhGbVdyeVFGRk9JWUVMancyUEI4ZDdPY19ua1l1YnRHQWxJMUNVUTBpQWt3RUNEa0JwQUEifQ.OBwDPTPqfQ-PO2qepY2Yv6uKRXX8DSLiMoQWL6Vqn6okZSkwQPUZhV6LWszUpgJa0evgICRlXZwPRCUqpz82sZcIoDrATKzFdXU1lI1sYLJGtUspWj9lycsYVgjfuV7Ubrs7EDVZbluZXuKIA2O2LAtNKcJHrjMfGXx0wVhxPlCNN7Ifeqr_CTtd-_5u8aF2nXivh-8jznV-G6UZ1m6qSC3dLCiLTXMn84GkbbDldB1EvsMsQmDQLi_thHv6IvRgW9Mv0Wu_d3hZiQXbXQ57qqSCFOoxCA4J0IuADuASeuAoHP1LTG61Aq7GXBqk6TuOndtyRGCXcjqajvWLtHL2UA'
    try:
        fetch_powerbi_workspaces(access_token,workspaces = ['f662fc65-5f19-4999-9d04-0d53d1c2a954'] )
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()