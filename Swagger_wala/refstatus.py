from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import requests
import uuid
import time  # To allow a short wait to fetch status
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

# Define request schema for a single dataset
class DatasetInput(BaseModel):
    groupId: str
    datasetId: str
    reportName: str

# Define request schema for multiple datasets
class ProcessDatasetsInput(BaseModel):
    datasets: List[DatasetInput]  # Input: List of multiple datasets


# Function to get refresh status
def get_refresh_status(
    group_id: str, dataset_id: str, request_id: str, access_token: str
) -> Dict[str, Any]:
    """
    Fetches the specific refresh status for a dataset based on the `requestId`.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    logger.info(
        f"Fetching refresh status for DatasetId: {dataset_id}, GroupId: {group_id}, RequestId: {request_id}"
    )

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            refresh_history = response.json().get("value", [])

            # Find the specific refresh entry using requestId
            matching_refresh = next(
                (refresh for refresh in refresh_history if refresh.get("requestId") == request_id), None
            )

            if matching_refresh:
                # If match is found, return rich metadata
                return {
                    "refreshId": matching_refresh.get("id"),
                    "status": matching_refresh.get("status"),  # e.g., InProgress, Completed, Failed
                    "refreshType": matching_refresh.get("refreshType"),  # e.g., ViaApi, Manual
                    "startTime": matching_refresh.get("startTime"),
                    "endTime": matching_refresh.get("endTime"),
                }
            else:
                # If no matching refresh is found
                return {
                    "status": "Unknown",
                    "requestId": request_id,
                    "error": f"No refresh entry found for RequestId: {request_id}",
                }
        else:
            # Log and raise HTTP exception for errors
            logger.error(f"Failed to fetch refresh status: HTTP {response.status_code}, Response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error fetching refresh status: {response.text}",
            )
    except requests.exceptions.RequestException as e:
        # Handle connection or request errors
        logger.error(f"RequestException while fetching status for DatasetId: {dataset_id}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch refresh status: {str(e)}")


# Function to trigger a refresh for multiple datasets and include their statuses
def trigger_refreshes(
    access_token: str, datasets: List[DatasetInput]
) -> List[Dict[str, Any]]:
    """
    Triggers refreshes for multiple datasets and retrieves their statuses.
    Returns the responses including datasetId, groupId, reportName, requestId, and refresh status.
    """
    responses = []
    for dataset in datasets:  # Loop through each provided dataset
        request_id = str(uuid.uuid4())  # Generate unique request ID for traceability
        url = f"{BASE_URL}/v1.0/myorg/groups/{dataset.groupId}/datasets/{dataset.datasetId}/refreshes"
        headers = {"Authorization": f"Bearer {access_token}"}
        headers["X-RequestId"] = request_id

        try:
            # Trigger dataset refresh
            logger.info(f"Triggering refresh for DatasetId: {dataset.datasetId}, GroupId: {dataset.groupId}")
            response = requests.post(url, headers=headers)

            if response.status_code == 202:  # Success
                # Wait briefly to allow the refresh entry to populate in the history
                time.sleep(2)

                # Fetch the refresh status using the requestId
                refresh_status = get_refresh_status(
                    dataset.groupId, dataset.datasetId, request_id, access_token
                )
                refresh_status.update(
                    {
                        "datasetId": dataset.datasetId,
                        "groupId": dataset.groupId,
                        "reportName": dataset.reportName,
                        "requestId": request_id,
                        "status": refresh_status,
                        "refreshTriggered": True,
                    }
                )
                responses.append(refresh_status)

            elif response.status_code == 400:  # Handle client error
                refresh_response = response.json()
                if refresh_response.get("error", {}).get("code") == "RefreshInProgressException":
                    responses.append(
                        {
                            "datasetId": dataset.datasetId,
                            "groupId": dataset.groupId,
                            "reportName": dataset.reportName,
                            "requestId": request_id,
                            "refreshTriggered": False,
                            "status": "InProgress",
                            "error": "Refresh already in progress",
                        }
                    )
                else:
                    responses.append(
                        {
                            "datasetId": dataset.datasetId,
                            "groupId": dataset.groupId,
                            "reportName": dataset.reportName,
                            "requestId": request_id,
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
                        "requestId": request_id,
                        "refreshTriggered": False,
                        "error": f"Error triggering refresh: {response.text}",
                    }
                )
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Failed to trigger refresh for DatasetId: {dataset.datasetId}, GroupId: {dataset.groupId}. Error: {str(e)}"
            )
            responses.append(
                {
                    "datasetId": dataset.datasetId,
                    "groupId": dataset.groupId,
                    "reportName": dataset.reportName,
                    "requestId": request_id,
                    "refreshTriggered": False,
                    "error": "Request failed, unable to trigger refresh.",
                }
            )

    return responses


# ====================================
# FastAPI Endpoints
# ====================================
@app.post("/trigger-refreshes-with-status/", summary="Trigger refreshes and fetch statuses for multiple datasets")
async def trigger_refreshes_with_status_endpoint(request: ProcessDatasetsInput):
    """
    Accepts an array of datasets, triggers refreshes for each dataset,
    and returns an array of structured responses including refresh statuses.
    """
    access_token = get_oauth2_token()  # Fetch the OAuth2 token dynamically

    # Trigger refreshes for multiple datasets and fetch their statuses
    results = trigger_refreshes(access_token, request.datasets)

    # Return the results as a structured response
    return {"results": results}