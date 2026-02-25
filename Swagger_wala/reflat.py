import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import requests
from datetime import datetime
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
    requestId: str

# Define input schema for multiple datasets
class ProcessDatasetsInput(BaseModel):
    datasets: List[DatasetInput]  # An array of dataset objects


# Get refresh history helper function
def refresh_history(
    group_id: str, dataset_id: str, request_id: str, access_token: str
) -> Dict[str, Any]:
    """
    Retrieves the latest refresh status for the given dataset and enriches the response
    with metadata like datasetId, groupId, and requestId.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    logger.info(f"Fetching refresh history from URL: {url}")
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse response and identify the most recent refresh
        data = response.json()
        refresh_history = data.get("value", [])
        if not refresh_history:
            # No refresh records found
            return {
                "datasetId": dataset_id,
                "groupId": group_id,
                "refreshAvailable": False,
                "message": "No refresh history found for this dataset.",
            }
        # Sort the history by startTime in descending order to find the most recent refresh
        latest_refresh = sorted(
            refresh_history,
            key=lambda x: datetime.fromisoformat(x["startTime"].replace("Z", "")),  # Sort by startTime
            reverse=True,
        )[0]
        # Find the specific refresh entry using requestId
        if latest_refresh.get("requestId", "N/A") == request_id:
            # Enrich the latest refresh with metadata
            response_obj = {
                "refreshId": latest_refresh.get("id"),
                "status": latest_refresh.get("status"),
                "requestId": latest_refresh.get("requestId"),
                "refreshType": latest_refresh.get("refreshType"),
                "startTime": latest_refresh.get("startTime"),
                "endTime": latest_refresh.get("endTime"),
                "datasetId": dataset_id,
                "groupId": group_id,
                "Reason": latest_refresh.get("serviceExceptionJson")
            }
            return response_obj
        else:
            return {
                "datasetId": dataset_id,
                "groupId": group_id,
                "requestId": request_id,
                "refreshAvailable": False,
                "message": "No matching refresh entry found for the given requestId.",
            }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error fetching refresh history: {response.text}",
        )


# FastAPI Endpoint for refresh history with an array of datasets
@app.post("/get-latest-refresh-history/", summary="Get the latest refresh status for multiple datasets")
async def get_latest_refresh_history(request: ProcessDatasetsInput):
    """
    Endpoint to return the latest refresh history for multiple datasets.
    It processes an array of datasets (groupId, datasetId, requestId) and retrieves their statuses.
    """
    logger.info("Fetching latest refresh status for multiple datasets.")
    # Fetch the OAuth2 token
    access_token = get_oauth2_token()
    # List to store all refresh statuses
    responses = []

    for dataset in request.datasets:  # Loop through the datasets array
        try:
            # Fetch the latest refresh history for each dataset
            latest_refresh_status = refresh_history(
                dataset.groupId, dataset.datasetId, dataset.requestId, access_token
            )
            responses.append(latest_refresh_status)
        except Exception as e:
            # Handle any errors for individual datasets
            logger.error(f"Error fetching refresh history for DatasetId {dataset.datasetId}: {str(e)}")
            responses.append({
                "datasetId": dataset.datasetId,
                "groupId": dataset.groupId,
                "requestId": dataset.requestId,
                "error": str(e),
            })

    return {"results": responses}