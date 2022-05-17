from fastapi import APIRouter
from app.utilities.dynamo_db import get_home_page_data
import logging



router = APIRouter(
    prefix = "/home_page",
    tags=["home_page_data"]
)

logger = logging.getLogger(__name__)

@router.get("/loans")
async def get_home_page_details(phone_number : str, sub_id: str):
    logger.info("Extracting data for appform id for home page: %s", phone_number)
    return get_home_page_data(phone_number,sub_id)
