import requests
#import pandas as pd


def fetch_powerbi_workspaces(access_token):
    # Define the API endpoint to retrieve modified workspaces
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified"
    
    # Set headers for the API request, including the access token for authentication
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Send a GET request to the Power BI API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        workspaces = response.json()
        if workspaces.get("success") and "data" in workspaces:
            # Convert the workspace data into a DataFrame
            #workspace_df = pd.DataFrame(workspaces["data"])
            print("Workspace Data:")
           # print(workspace_df)
            
            # Save the DataFrame to an Excel file
            excel_file_name = 'workspaces_data.xlsx'
            workspace_df.to_excel(excel_file_name, index=False)
            print(f"Workspace data saved to {excel_file_name}")
        else:
            print("No workspace data found or the request was not successful.")
    else:
        print(f"Unable to retrieve workspaces. Status code: {response.status_code}, Message: {response.text}")

def main():
    # Replace with your own access token obtained through the OAuth 2.0 authentication flow
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkhTMjNiN0RvN1RjYVUxUm9MSHdwSXEyNFZZZyIsImtpZCI6IkhTMjNiN0RvN1RjYVUxUm9MSHdwSXEyNFZZZyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNTc5NjBkM2UtNzdkYS00MDE3LTlkYmUtNGNiYjdkNmE3MTk0LyIsImlhdCI6MTc1ODc4NDA1OSwibmJmIjoxNzU4Nzg0MDU5LCJleHAiOjE3NTg3ODc5NTksImFpbyI6ImsyUmdZRmhrTXlPL2VPWGFsQnIyZ0RXdk9mKzlBQUE9IiwiYXBwaWQiOiJiZDhhNTdiNC1hNzU0LTRkNjktODZjYy1mMGNlM2UxNjRlNzkiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81Nzk2MGQzZS03N2RhLTQwMTctOWRiZS00Y2JiN2Q2YTcxOTQvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiJlYWQ1YjhkMC05MWE0LTRkODMtOTJkZS0wMjMxOWIzNjc3YWEiLCJyaCI6IjEuQVQ0QVBnMldWOXAzRjBDZHZreTdmV3B4bEFrQUFBQUFBQUFBd0FBQUFBQUFBQURIQUFBLUFBLiIsInN1YiI6ImVhZDViOGQwLTkxYTQtNGQ4My05MmRlLTAyMzE5YjM2NzdhYSIsInRpZCI6IjU3OTYwZDNlLTc3ZGEtNDAxNy05ZGJlLTRjYmI3ZDZhNzE5NCIsInV0aSI6IkFkTl9fS0dTVUVDTV8ycDZZSFB6QUEiLCJ2ZXIiOiIxLjAiLCJ4bXNfZnRkIjoic25Lb0stOXlpUWExRXZucHRpVkZ5a0h0RktjdXJWZ0Ria2YyQWo5VGh6a0JhMjl5WldGemIzVjBhQzFrYzIxeiIsInhtc19pZHJlbCI6IjcgMzIiLCJ4bXNfcmQiOiIwLjQyTGxZQkppdEJNUzRXQVhFdmhXeVMzNUlFZlB1X1ZWNHZIRm1XcnlRRkZPSVlFTGp3MlBCOGQ3T2NfbmtZdWJ0R0FsSTFDVVEwaUFrd0VDRGtCcEFBIn0.g2sP4HrUqOgV38uB6q5HulGd808yk6buOf3JyBhX9OuBM4GY5TR7ce734UU8kxq9I_WrCBb83gLhiFa43-QetgmMRYD9EBykEz5tt3WginLZDItvuru4N4NsWt55HPfVWwp8KkMlS0q22uAdSAPLHBY-5RjZ0WAHBzUfwyXVDfrnXGol4B5EJ4V6DPJPvK0OcxXod95K_slnP3s3JzKnlA5A9Zt5-CEW39dQJHAItf55_HapGnBSp7bjxFp0nF7VmOYeTfv4ZqwS9ha94vMZVtYy5Fb70ANJcSOtGL--sBM6K4L-esZFEgmkyUNY5eJ-iidPo3eSjGjOeoj_X0lyPw'
    
    try:
        fetch_powerbi_workspaces(access_token)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()