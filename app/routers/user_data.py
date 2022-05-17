from fastapi import APIRouter, Body
from app.utilities.dynamo_db import get_all_appform_data, get_appform_data
import json



router = APIRouter(
    prefix = "/appform",
    tags=["appform_data"]
)


@router.get("/{app_form_id}")
async def get_appform_data_one(app_form_id):
    print("Extracting data for appform id : "+app_form_id)
    return get_appform_data(app_form_id)

@router.get("/get/allappform")
async def get_appform_data_all(fromdate: str,todate: str):
    print("Extracting bulk appform data")
    return json.loads(get_all_appform_data(fromdate,todate))