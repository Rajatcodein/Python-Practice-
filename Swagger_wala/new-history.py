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
logger = logging.getLogger("app_logger")

# FastAPI instance
app = FastAPI()

# Define request schema for each dataset
class DatasetInput(BaseModel):
    groupId: str
    datasetId: str
    requestId: str

# Function to trigger refresh
def trigger_refresh(
    access_token: str,
    dataset_id: str,
    group_id: str,
    report_name: str,
    all_responses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Triggers a dataset refresh and returns the response object.
    Appends the response to the global `all_responses` list.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    request_id = str(uuid.uuid4())
    if response.status_code == 202:  # Refresh triggered successfully
        refresh_response = {
            "reportName": report_name,
            "datasetId": dataset_id,
            "groupId": group_id,
            "requestId": request_id,
            "refreshTriggered": True,
        }
        all_responses.append(refresh_response)
        return refresh_response
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error triggering refresh: {response.text}",
        )

# Function to fetch the latest refresh history
def fetch_latest_refresh_history(
    group_id: str, dataset_id: str, request_id: str, access_token: str
) -> Dict[str, Any]:
    """
    Retrieves the latest refresh status for a dataset and enriches the response 
    with relevant metadata such as datasetId, groupId, and requestId.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    logger.info(f"Fetching refresh history from: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse response and fetch refresh history
        data = response.json()
        refresh_history = data.get("value", [])
        if not refresh_history:
            return {
                "datasetId": dataset_id,
                "groupId": group_id,
                "refreshAvailable": False,
                "message": "No refresh history found for this dataset.",
            }
        
        # Get the most recent refresh based on startTime
        latest_refresh = sorted(
            refresh_history,
            key=lambda x: datetime.fromisoformat(x["startTime"].replace("Z", "")),  # Sort by startTime
            reverse=True,
        )[0]

        # Build the response object using the latest refresh data
        response_obj = {
            "refreshId": latest_refresh.get("id"),
            "status": latest_refresh.get("status"),
            "requestId": latest_refresh.get("requestId", request_id),
            "refreshType": latest_refresh.get("refreshType"),
            "startTime": latest_refresh.get("startTime"),
            "endTime": latest_refresh.get("endTime"),
            "datasetId": dataset_id,
            "groupId": group_id,
        }
        return response_obj
    else:
        logger.error(f"Failed to fetch refresh history: {response.text}")
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error fetching refresh history: {response.text}",
        )

# FastAPI Endpoint that accepts and returns an array of dataset objects
@app.post("/get-latest-refresh-history/", summary="Get latest refresh status for multiple datasets")
async def get_latest_refresh_history(datasets: List[DatasetInput]):
    """
    Accepts an array of dataset objects, retrieves the latest refresh status for each dataset,
    and returns a corresponding array of refresh status objects.
    """
    # Log the size of the input
    logger.info(f"Received request to fetch latest refresh history for {len(datasets)} datasets.")

    # Fetch the access token
    access_token = get_oauth2_token()

    # Prepare the output as an array of responses
    results = []
    for dataset in datasets:
        # Fetch the latest refresh history for each dataset
        try:
            latest_status = fetch_latest_refresh_history(
                group_id=dataset.groupId,
                dataset_id=dataset.datasetId,
                request_id=dataset.requestId,
                access_token=access_token
            )
            results.append(latest_status)
        except HTTPException as e:
            # If fetching history fails, append the error for that specific dataset
            results.append({
                "datasetId": dataset.datasetId,
                "groupId": dataset.groupId,
                "requestId": dataset.requestId,
                "error": str(e.detail)
            })

    # Return the array of responses
    return {"results": results}