from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
import time
import requests
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

# Define request schema for validation
class DatasetInput(BaseModel):
    groupId: str
    datasetId: str
    reportName: str

# Define request schema for multiple datasets
class ProcessDatasetsInput(BaseModel):
    datasets: List[DatasetInput]

# Trigger Refresh function
def trigger_refresh(
    access_token: str, dataset_id: str, group_id: str, report_name: str
) -> Dict[str, Any]:
    """
    Triggers a dataset refresh and returns the response object.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)

    if response.status_code == 202:  # Success
        return {
            "reportName": report_name,
            "datasetId": dataset_id,
            "groupId": group_id,
            
            "refreshTriggered": True,
        }
    elif response.status_code == 400:  # Handle client error
        refresh_response = response.json()
        if refresh_response.get("error", {}).get("code") == "RefreshInProgressException":
            return {
                "reportName": report_name,
                "datasetId": dataset_id,
                "groupId": group_id,
                "refreshTriggered": False,
                "error": "Refresh already in progress",
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error triggering refresh: {refresh_response}",
            )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error triggering refresh: {response.text}",
        )

# Get Refresh History function
def get_dataset_refreshes(
    group_id: str, dataset_id: str, report_name: str, access_token: str
) -> List[Dict[str, Any]]:
    """
    Gets dataset refresh history with additional reportName, datasetId, and groupId details.
    Returns the refresh history as a list of objects.
    """
    url = f"{BASE_URL}/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    logger.info(f"Fetching refresh history from URL: {url}")

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse response and enrich with additional details
        data = response.json()
        refresh_history = [
            {
                "refreshId": refresh.get("id"),
                "status": refresh.get("status"),
                "requestId": refresh.get("requestId", "N/A"),
                "refreshType": refresh.get("refreshType"),
                "startTime": refresh.get("startTime"),
                "endTime": refresh.get("endTime"),
                "reportName": report_name,
                "datasetId": dataset_id,
                "groupId": group_id,
            }
            for refresh in data.get("value", [])
        ]
        return refresh_history
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error fetching refresh history: {response.text}",
        )

# Process Datasets function
def process_datasets(dataset_list: List[DatasetInput]) -> List[Dict[str, Any]]:
    """
    Trigger refresh and fetch refresh history for multiple datasets.
    """
    results = []
    access_token = get_oauth2_token()  # Get the OAuth2 token dynamically

    for dataset in dataset_list:
        try:
            # Extract individual dataset attributes
            group_id = dataset.groupId
            dataset_id = dataset.datasetId
            report_name = dataset.reportName

            # Step 1: Trigger a refresh for the dataset
            refresh_result = trigger_refresh(
                access_token, dataset_id, group_id, report_name
            )
            results.append(refresh_result)

            if not refresh_result.get("refreshTriggered"):
                # Skip history fetching if refresh wasn't triggered
                continue

            # Step 2: Fetch refresh history (wait 1 second to avoid throttling)
            time.sleep(1)
            refresh_history = get_dataset_refreshes(
                group_id, dataset_id, report_name, access_token
            )
            results.extend(refresh_history)

        except Exception as e:
            # Catch errors for individual datasets and log them
            logger.error(f"Error processing dataset {dataset.datasetId}: {str(e)}")
            results.append(
                {"reportName": report_name, "datasetId": dataset_id, "groupId": group_id, "error": str(e)}
            )

    return results

# ====================================
# FastAPI Endpoints
# ====================================

# 1. Trigger refresh for a single dataset
@app.post("/trigger-refresh/", summary="Trigger a dataset refresh")
async def trigger_refresh_endpoint(request: DatasetInput):
    access_token = get_oauth2_token()  # Get the OAuth2 token
    result = trigger_refresh(
        access_token=access_token,
        dataset_id=request.datasetId,
        group_id=request.groupId,
        report_name=request.reportName,
    )
    return result

# 2. Fetch refresh history for a single dataset
@app.get("/get-refresh-history/", summary="Get refresh history for a dataset")
async def get_refresh_history(groupId: str, datasetId: str, reportName: str):
    """
    Returns the refresh history for a single dataset as a list of objects.
    Each object contains `refreshId`, `status`, `requestId`, `refreshType`, `reportName`,
    `datasetId`, and `groupId`.
    """
    logger.info(f"Fetching refresh history for DatasetId: {datasetId}, GroupId: {groupId}")
    access_token = get_oauth2_token()  # Get the OAuth2 token
    refresh_history = get_dataset_refreshes(groupId, datasetId, reportName, access_token)
    return {"refreshHistory": refresh_history}

# 3. Process multiple datasets: Trigger refreshes and fetch history
@app.post("/process-datasets/", summary="Process multiple datasets: Trigger refreshes and fetch history")
async def process_datasets_endpoint(request: ProcessDatasetsInput):
    dataset_list = request.datasets
    results = process_datasets(dataset_list)
    return {"results": results}