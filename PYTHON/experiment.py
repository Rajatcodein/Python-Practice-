import requests
import time

def get_oauth2_token():
    """
    Fetch the OAuth2 token for authentication.
    """
    client_id = "bd8a57b4-a754-4d69-86cc-f0ce3e164e79"
    client_secret = "pLX8Q~4uQSz2R_49aL4ny2dGiHoQIlre5j6gqbDc"
    tenant_id = "57960d3e-77da-4017-9dbe-4cbb7d6a7194"
    scope = "https://analysis.windows.net/powerbi/api/.default"
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope={scope}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    response = requests.post(url, headers=headers, data=payload) 
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error obtaining token: {response.status_code}, {response.text}")

def trigger_refresh(dataset_id, group_id):
    """
    Trigger a refresh for the given dataset and group.
    """
    access_token = get_oauth2_token()  
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        print(f"Refresh triggered for dataset_id: {dataset_id} in group_id: {group_id}")
        return True
    elif response.status_code == 400:
        refresh_response = response.json()
        if refresh_response.get("error").get("code") == "RefreshInProgressException":
            print(f"Refresh already in progress for dataset_id: {dataset_id} in group_id: {group_id}")
            return False
        else:
            print(f"Other error during refresh: {refresh_response}")
    else:
        raise Exception(f"Error triggering refresh for dataset {dataset_id}: {response.status_code}, {response.text}")
    return False

def get_dataset_refreshes(group_id, dataset_id, access_token):
    """
    Fetch the refresh history for a given dataset and group.
    """
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse response JSON for refresh details
        data = response.json()
        refresh_ids = [
            (refresh['id'], refresh['status'], refresh.get('requestId', 'N/A'), refresh['refreshType'])
            for refresh in data.get('value', [])
        ]
        return refresh_ids
    else:
        print(f"Error fetching refresh history: {response.status_code}, {response.text}")
        return None

def process_datasets(dataset_list):
   
    results = []

    for dataset in dataset_list:
        # Extract details from the dataset object
        group_id = dataset.get("groupId")
        dataset_id = dataset.get("datasetId")
        report_name = dataset.get("reportName")

        if not group_id or not dataset_id or not report_name:
            print(f"Invalid dataset object: {dataset}")
            continue

        try:
            # Step 1: Trigger the refresh API
            print(f"Triggering refresh for report: {report_name}, groupId: {group_id}, datasetId: {dataset_id}")
            refresh_triggered = trigger_refresh(dataset_id, group_id)
            if not refresh_triggered:
                print(f"Skipping refresh history fetch for report: {report_name}")
                continue

            
            time.sleep(5)

            
            access_token = get_oauth2_token()
            refresh_ids = get_dataset_refreshes(group_id, dataset_id, access_token)

           
            if refresh_ids:
                for refresh_id, status, request_id, refresh_type in refresh_ids:
                    if refresh_type == "ViaApi":
                        print(f"Report: {report_name}, Refresh ID: {refresh_id}, Status: {status}, Request ID: {request_id}")
                        results.append({
                            "reportName": report_name,
                            "refreshId": refresh_id,
                            "status": status,
                            "requestId": request_id
                        })
                        break 
            else:
                print(f"No refresh history available for report: {report_name}")
        except Exception as e:
            print(f"Error processing report: {report_name}. Error: {str(e)}")
    
    return results

def main():
    """
    Main function to execute the dataset refresh and get refresh history.
    """
    # Sample input: Replace this with actual input
    dataset_list = [
        {"groupId": "group_id_1", "datasetId": "dataset_id_1", "reportName": "Sales Report"},
        {"groupId": "group_id_2", "datasetId": "dataset_id_2", "reportName": "Marketing Report"},
        {"groupId": "group_id_3", "datasetId": "dataset_id_3", "reportName": "Finance Report"},
    ]
    
    # Process the dataset list
    refresh_results = process_datasets(dataset_list)
    
    # Log the results
    print("\nFinal Results:")
    for result in refresh_results:
        print(f"Report: {result['reportName']}, Refresh ID: {result['refreshId']}, Status: {result['status']}, Request ID: {result['requestId']}")

# Run the main function
if __name__ == "__main__":
    main()