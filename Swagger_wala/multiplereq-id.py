import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import requests
from datetime import datetime
from auth.get_token import get_oauth2_token
from constant.contant import BASE_URL


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("app")

# Initialize FastAPI application
app = FastAPI()


# Request schema for a single dataset
class DatasetRequest(BaseModel):
    groupId: str        # Group ID of the dataset
    datasetId: str      # ID of the dataset
    requestIds: List[str]  # List of request IDs for this dataset


@app.post("/get-dataset-refresh-history/", summary="Get refresh history for a specific dataset and multiple requestIds")
async def get_dataset_refresh_history(request: DatasetRequest):
    """
    Fetches refresh history for a specific dataset and matches multiple request IDs.
    """
    access_token = get_oauth2_token()  # Retrieve OAuth2 token for Power BI API
    group_id, dataset_id, request_ids = request.groupId, request.datasetId, request.requestIds
    logger.info(f"Processing refresh history for groupId: {group_id}, datasetId: {dataset_id}")

    # Call helper function to fetch refreshes matching the provided request IDs
    matched_refreshes = fetch_history_by_request_ids(group_id, dataset_id, request_ids, access_token)

    # Return response
    if not matched_refreshes:
        return {
            "message": "No refresh history entries matched the provided request IDs.",
            "results": []
        }
    return {"results": matched_refreshes}


# Fetch refresh history for a dataset and filter by request IDs
def fetch_history_by_request_ids(group_id: str, dataset_id: str, request_ids: List[str], access_token: str) -> List[Dict[str, Any]]:
    """
    Fetches refresh history and filters the entries by request IDs.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}"}
    logger.info(f"Requesting refresh history from URL: {url}")

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        refresh_history = response.json().get("value", [])
        if not refresh_history:
            return []

        # Filter refresh history for matches with request IDs
        matches = [
            {
                "refreshId": refresh.get("id"),
                "status": refresh.get("status"),
                "requestId": refresh.get("requestId"),
                "refreshType": refresh.get("refreshType"),
                "startTime": refresh.get("startTime"),
                "endTime": refresh.get("endTime"),
                "datasetId": dataset_id,
                "groupId": group_id,
            }
            for refresh in refresh_history if refresh.get("requestId") in request_ids
        ]
        return matches

    except requests.exceptions.RequestException as e:
        logger.error(f"Error while fetching refresh history for DatasetId {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve refresh history: {e}")