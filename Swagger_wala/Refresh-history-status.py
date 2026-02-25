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

# Define the schema for multiple datasets
class ProcessDatasetsInput(BaseModel):
    datasets: List[DatasetInput]


# Function to fetch refresh history and match requestId
def fetch_refresh_history_and_match(
    group_id: str, dataset_id: str, request_id: str, access_token: str
) -> Dict[str, Any]:
    """
    Fetch refresh history and find the entry that matches the given `requestId`.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    logger.info(f"Fetching refresh history for DatasetId: {dataset_id}, GroupId: {group_id} and RequestId: {request_id}")
    
    try:
        response = requests.get(url, headers=headers)
        logger.info(response)
        if response.status_code == 200:
            # Extract the refresh history
            refresh_history = response.json().get("value", [])
            

            # Match the specific requestId
            for refresh in refresh_history:
                if refresh.get("requestId") == request_id:
                    # Found a match, return the refresh details
                    return {
                        "refreshId": refresh.get("id"),
                        "status": refresh.get("status"),
                        "requestId": refresh.get("requestId"),
                        "refreshType": refresh.get("refreshType"),
                        "startTime": refresh.get("startTime"),
                        "endTime": refresh.get("endTime"),
                        "datasetId": dataset_id,
                        "groupId": group_id,
                    }

            # Return error if no matches are found
            return {
                "datasetId": dataset_id,
                "groupId": group_id,
                "requestId": request_id,
                "message": "No matching refresh ID found for the provided requestId."
            }
        else:
            logger.error(f"Failed to fetch refresh history: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"API Error: {response.text}")
    except Exception as e:
        logger.error(f"An error occurred when fetching refresh history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve refresh history.")


# Function to process multiple datasets and match requestId for each
def process_datasets_and_match(access_token: str, datasets: List[DatasetInput]) -> List[Dict[str, Any]]:
    """
    Process multiple dataset inputs, fetch their refresh history, and match the requestId for each.
    """
    results = []
    
    for dataset in datasets:
        try:
            # Fetch and match the refresh history for each dataset and requestId
            match = fetch_refresh_history_and_match(
                group_id=dataset.groupId,
                dataset_id=dataset.datasetId,
                request_id=dataset.requestId,
                access_token=access_token,
            )
            results.append(match)  # Add the match (or error) to the results
        except Exception as e:
            logger.error(f"Error processing DatasetId {dataset.datasetId}. Error: {str(e)}")
            results.append({
                "datasetId": dataset.datasetId,
                "groupId": dataset.groupId,
                "requestId": dataset.requestId,
                "error": str(e),
            })

    return results


# FastAPI Endpoint for handling arrays of objects
@app.post("/get-datasets-refresh-status/", summary="Get refresh statuses for multiple datasets")
async def get_datasets_refresh_status(request: ProcessDatasetsInput):
    """
    Endpoint to return refresh statuses for multiple datasets.
    """
    logger.info("Processing refresh history for multiple datasets.")
    # Fetch OAuth2 access token dynamically
    access_token = get_oauth2_token()

    # Process all datasets and return the matches for their requestIds
    results = process_datasets_and_match(access_token, request.datasets)

    return {"results": results}