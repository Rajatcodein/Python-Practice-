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

# Define request schema for single dataset
class DatasetInput(BaseModel):
    groupId: str
    datasetId: str
    requestId: str

# Trigger Refresh function
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
    if response.status_code == 202:  # Success
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

# Get refresh history helper function
def fetch_latest_refresh_history(
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

        # Enrich the latest refresh with metadata
        response_obj = {
            "refreshId": latest_refresh.get("id"),
            "status": latest_refresh.get("status"),
            "requestId": latest_refresh.get("requestId", "N/A"),
            "refreshType": latest_refresh.get("refreshType"),
            "startTime": latest_refresh.get("startTime"),
            "endTime": latest_refresh.get("endTime"),
            "datasetId": dataset_id,
            "groupId": group_id,
        }
        return response_obj
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error fetching refresh history: {response.text}",
        )

# FastAPI Endpoint for refresh history
@app.get("/get-latest-refresh-history/", summary="Get the latest refresh status for a dataset")
async def get_latest_refresh_history(groupId: str, datasetId: str, requestId: str):
    """
    Endpoint to return the latest refresh history of a dataset using groupId, datasetId, and requestId.
    """
    logger.info(f"Fetching latest refresh status for DatasetId: {datasetId}, GroupId: {groupId}")

    # Fetch the OAuth2 token
    access_token = get_oauth2_token()

    # Fetch the latest refresh history using the updated helper function
    latest_refresh_status = fetch_latest_refresh_history(groupId, datasetId, requestId, access_token)

    return {"latestRefreshStatus": latest_refresh_status}