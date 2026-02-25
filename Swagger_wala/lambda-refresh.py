from constant.contant import BASE_URL
import requests
from typing import List, Dict, Any
import uuid
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

def trigger_refresh(access_token: str, datasets: List):

    """
    Triggers dataset refreshes for multiple datasets.
    Returns the responses as a list of objects (each containing datasetId, groupId, reportName, and requestId).
    """
    responses = []
    for dataset in datasets:  # Loop through each provided dataset
        url = f"{BASE_URL}/v1.0/myorg/groups/{dataset.groupId}/datasets/{dataset.datasetId}/refreshes"
        headers = {"Authorization": f"Bearer {access_token}"}

        # Generate a unique request ID for each refresh (client-side identifier)
        client_request_id = str(uuid.uuid4())
        headers["X-RequestId"] = client_request_id  # Optional: Provide requestId in headers for traceability

        try:
            response = requests.post(url, headers=headers)
            server_request_id = response.headers.get("RequestId")  # Extract requestId from response headers (if provided)

            if response.status_code == 202:  # Success
                responses.append(
                    {
                        "datasetId": dataset.datasetId,
                        "groupId": dataset.groupId,
                        "reportName": dataset.reportName,
                        #"clientRequestId": client_request_id,  # Include the client-side request ID
                        "serverRequestId": server_request_id,  # Include the server-side request ID
                        "refreshTriggered": True,
                    }
                )
            elif response.status_code == 400:  # Handle client error
                refresh_response = response.json()
                if refresh_response.get("error", {}).get("code") == "RefreshInProgressException":
                    responses.append(
                        {
                            "datasetId": dataset.datasetId,
                            "groupId": dataset.groupId,
                            "reportName": dataset.reportName,
                            #"clientRequestId": client_request_id,
                            "serverRequestId": server_request_id,
                            "refreshTriggered": False,
                            "error": "Refresh already in progress",
                        }
                    )
                else:
                    responses.append(
                        {
                            "datasetId": dataset.datasetId,
                            "groupId": dataset.groupId,
                            "reportName": dataset.reportName,
                            #"clientRequestId": client_request_id,
                            "serverRequestId": server_request_id,
                            "refreshTriggered": False,
                            "error": f"Error triggering refresh: {refresh_response}",
                        }
                    )
            else:
                responses.append(
                    {
                        "datasetId": dataset.datasetId,
                        "groupId": dataset.groupId,
                        "reportName": dataset.reportName,
                        #"clientRequestId": client_request_id,
                        "serverRequestId": server_request_id,
                        "refreshTriggered": False,
                        "error": f"Error triggering refresh: {response.text}",
                    }
                )
        except requests.exceptions.RequestException as e:
            print(f"Failed to trigger refresh for DatasetId: {dataset.datasetId}. Error: {str(e)}")
            responses.append(
                {
                    "datasetId": dataset.datasetId,
                    "groupId": dataset.groupId,
                    "reportName": dataset.reportName,
                    #"clientRequestId": client_request_id,
                    "serverRequestId": None,  # No server-level request ID available in case of exceptions
                    "refreshTriggered": False,
                    "error": "Request failed, unable to trigger refresh.",
                }
            )
    return responses