from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import requests
import uuid
from auth.get_token import get_oauth2_token
from constant.contant import BASE_URL

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("app")

# Initialize FastAPI
app = FastAPI()

# Define request schema for single dataset
class DatasetInput(BaseModel):
    groupId: str
    datasetId: str
    reportName: str

# Define request schema for multiple datasets
class ProcessDatasetsInput(BaseModel):
    datasets: List[DatasetInput]  # Input: List of multiple datasets

# Function to trigger a refresh for multiple datasets
def trigger_refresh(
    access_token: str, datasets: List[DatasetInput]
) -> List[Dict[str, Any]]:
    """
    Triggers dataset refreshes for multiple datasets.
    Returns the responses as a list of objects (each containing datasetId, groupId, reportName, and requestId).
    """
    responses = []
    for dataset in datasets:  # Loop through each provided dataset
        url = f"{BASE_URL}/v1.0/myorg/groups/{dataset.groupId}/datasets/{dataset.datasetId}/refreshes"
        headers = {"Authorization": f"Bearer {access_token}"}

        

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
                        "RequestId": server_request_id,  # Include the server-side request ID
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
                            "RequestId": server_request_id,
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
                            "RequestId": server_request_id,
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
                        "RequestId": server_request_id,
                        "refreshTriggered": False,
                        "error": f"Error triggering refresh: {response.text}",
                    }
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to trigger refresh for DatasetId: {dataset.datasetId}. Error: {str(e)}")
            responses.append(
                {
                    "datasetId": dataset.datasetId,
                    "groupId": dataset.groupId,
                    "reportName": dataset.reportName,
                    #"clientRequestId": client_request_id,
                    "RequestId": None,  # No server-level request ID available in case of exceptions
                    "refreshTriggered": False,
                    "error": "Request failed, unable to trigger refresh.",
                }
            )
    return responses


# Process multiple datasets: Trigger refreshes and return request IDs
@app.post("/trigger-multiple-refreshes/", summary="Trigger refreshes for multiple datasets")
async def trigger_multiple_refreshes_endpoint(request: ProcessDatasetsInput):
    """
    Accepts an array of datasets, triggers refreshes for each of those datasets, and returns array responses.
    """
    access_token = get_oauth2_token()  # Fetch the OAuth2 token dynamically
    # Call the function to trigger refreshes for multiple datasets
    results = trigger_refresh(access_token, request.datasets)
    return {"results": results}