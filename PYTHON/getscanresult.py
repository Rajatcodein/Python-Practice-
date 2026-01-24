import requests
import csv


def fetch_powerbi_Scan_result(access_token,workspaces):
    url =" https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanResult/c221917b-a0e3-4c6f-b966-eaa0c63d7b52"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print(response)

    if response.status_code == 200:
        workspaces = response.json()
        print("status id",workspaces)
        if 'id' in workspaces:
             csv_file = [{
                'name': workspace.get('name'),
                'id': workspace.get('id'),
                'report created at': workspace.get('createdDateTime'),
                'modified': workspace.get('lastModified'),
                'modified by': workspace.get('lastModifiedBy')
            } for workspace in workspaces]
    csv_file(workspaces)
    for workspaces in workspaces:

            print(f"Workspace status : {workspaces['id']}")
    else:
        print(f"Failed to fetch workspaces. Status code: {response.status_code}, Message: {response.text}")
def csv_file(workspaces):
    csv_filename=workspaces
    csv_filename = 'workspaces_data.csv'
    with open(csv_filename, mode='w', newline='') as csvfile:
        fieldnames = workspaces[0].keys()
        print(fieldnames) 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 
        for workspace in workspaces:
            writer.writerow(workspace)
    print(fieldnames) 
        
    print(f"Data has been successfully saved to {csv_filename}.")
def main():
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkhTMjNiN0RvN1RjYVUxUm9MSHdwSXEyNFZZZyIsImtpZCI6IkhTMjNiN0RvN1RjYVUxUm9MSHdwSXEyNFZZZyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNTc5NjBkM2UtNzdkYS00MDE3LTlkYmUtNGNiYjdkNmE3MTk0LyIsImlhdCI6MTc1ODc5MzAxMCwibmJmIjoxNzU4NzkzMDEwLCJleHAiOjE3NTg3OTY5MTAsImFpbyI6ImsyUmdZSGh4MXROOXk2cFFFLy9xV3JlbzYzdHRBUT09IiwiYXBwaWQiOiJiZDhhNTdiNC1hNzU0LTRkNjktODZjYy1mMGNlM2UxNjRlNzkiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81Nzk2MGQzZS03N2RhLTQwMTctOWRiZS00Y2JiN2Q2YTcxOTQvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiJlYWQ1YjhkMC05MWE0LTRkODMtOTJkZS0wMjMxOWIzNjc3YWEiLCJyaCI6IjEuQVQ0QVBnMldWOXAzRjBDZHZreTdmV3B4bEFrQUFBQUFBQUFBd0FBQUFBQUFBQURIQUFBLUFBLiIsInN1YiI6ImVhZDViOGQwLTkxYTQtNGQ4My05MmRlLTAyMzE5YjM2NzdhYSIsInRpZCI6IjU3OTYwZDNlLTc3ZGEtNDAxNy05ZGJlLTRjYmI3ZDZhNzE5NCIsInV0aSI6IkRLUlJHTnVic0VlOFEySmM3aHo2QUEiLCJ2ZXIiOiIxLjAiLCJ4bXNfZnRkIjoiVl9udkJZTWpsalQxRmxyalJEdGdPODhiY2dnbzAyRXg0MmxqWnlDT2pqb0JhbUZ3WVc1bFlYTjBMV1J6YlhNIiwieG1zX2lkcmVsIjoiMzAgNyIsInhtc19yZCI6IjAuNDJMbFlCSml0Qk1TNFdBWEV2aFd5UzM1SUVmUHVfVlY0dkhGbVdyeVFGRk9JWUVMancyUEI4ZDdPY19ua1l1YnRHQWxJMUNVUTBpQWt3RUNEa0JwQUEifQ.LbLnW5PfoTupSBu-Z9FBrus7yRrLwabumrVVOjONab-JDYay_x08m4avoHjKl1A_ovvoUyCdZ_CVWYC6aBavLnKmt6fN519OjH8hQiziPpHeU733OC9UPaGI5DzxEE3MMscDCo1WEBsfSJ3heC4uv_DBI2fBmfTZ04HkGzcMx91YW6wwLzm_P6Z_CINj_POzkmY2Hl7Sf3t38lrBK87njo79YULSiiMjAt7OO6axjwWiAHLN2Adt8KKMu67Hcz9k_avMVxCH73qOtTViuCqfT-64yywvI-OgDMYL8VZz66ApunjnZACG5xikxcDMyP2_0f88_v1LcAyl_sRKM0zxqw'
    #scanId = "1d4208f8-3d2c-42e1-8878-87073eceaedb"
    try:
        fetch_powerbi_Scan_result(access_token,workspaces='42896f9-fb00-4cd7-a36a-6ac00079d732')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
