from constant.contant import BASE_URL
import requests
import time
from auth.get_token import get_oauth2_token

def trigger_refresh(access_token, dataset_id, group_id, report_name):
    """
    Trigger a refresh for the given dataset and group.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 202:  # Success
        print(f"Refresh triggered for report: {report_name}, dataset_id: {dataset_id}, group_id: {group_id}")
        return {
            "reportName": report_name,
            "datasetId": dataset_id,
            "groupId": group_id,
            "refreshTriggered": True
        }
    elif response.status_code == 400:  # Error
        refresh_response = response.json()
        if refresh_response.get("error", {}).get("code") == "RefreshInProgressException":
            print(f"Refresh already in progress for report: {report_name}, dataset_id: {dataset_id}, group_id: {group_id}")
            return {
                "reportName": report_name,
                "datasetId": dataset_id,
                "groupId": group_id,
                "refreshTriggered": False,
                "error": "RefreshInProgressException"
            }
        else:
            print(f"Other error during refresh for dataset_id: {dataset_id}. Error: {refresh_response}")
            raise Exception(f"Error triggering refresh: {refresh_response}")
    else:
        raise Exception(f"Error triggering refresh for dataset {dataset_id}: {response.status_code}, {response.text}")

def get_dataset_refreshes(group_id, dataset_id, access_token):
    """
    Fetch the refresh history for a given dataset and group.
    Return the list of refresh details or None in case of an error.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the response JSON for refresh details
        data = response.json()
        refresh_details = [
            (refresh['id'], refresh['status'], refresh.get('requestId', 'N/A'), refresh['refreshType'])
            for refresh in data.get('value', [])
        ]
        return refresh_details
    else:
        print(f"Error fetching refresh history: {response.status_code}, {response.text}")
        return None

def process_datasets(dataset_list):
    """
    Process the datasets: Trigger refresh and fetch refresh history.
    """
    results = []
    access_token = get_oauth2_token()

    for dataset in dataset_list:
        group_id = dataset.get("groupId")
        dataset_id = dataset.get("datasetId")
        report_name = dataset.get("reportName")
        if not group_id or not dataset_id or not report_name:
            print(f"Invalid dataset object: {dataset}")
            continue

        try:
            # Step 1: Trigger the refresh
            print(f"Triggering refresh for report: {report_name}, groupId: {group_id}, datasetId: {dataset_id}")
            refresh_result = trigger_refresh(access_token, dataset_id, group_id, report_name)

            if not refresh_result.get("refreshTriggered", False):
                print(f"Skipping refresh history fetch for report: {report_name}")
                results.append(refresh_result)
                continue

            # Step 2: Fetch refresh history (optional delay to avoid API throttling)
            time.sleep(1)

            refresh_history = get_dataset_refreshes(group_id, dataset_id, access_token)

            if refresh_history:
                for refresh_id, status, request_id, refresh_type in refresh_history:
                    if refresh_type == "ViaApi":
                        print(f"Report: {report_name}, Refresh ID: {refresh_id}, Status: {status}, Request ID: {request_id}")
                        results.append({
                            "reportName": report_name,
                            "datasetId": dataset_id,
                            "groupId": group_id,
                            "refreshId": refresh_id,
                            "status": status,
                            "requestId": request_id,
                        })
                        break
            else:
                print(f"No refresh history available for report: {report_name}")
                results.append({
                    "reportName": report_name,
                    "datasetId": dataset_id,
                    "groupId": group_id,
                    "refreshHistoryAvailable": False
                })
        except Exception as e:
            print(f"Error processing report: {report_name}. Error: {str(e)}")
            results.append({
                "reportName": report_name,
                "datasetId": dataset_id,
                "groupId": group_id,
                "error": str(e)
            })

    return results