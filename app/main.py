from fastapi import FastAPI
import logging, time, random
from requests import Request
import string


from .routers import user_data, home_page_api


# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(user_data.router)
app.include_router(home_page_api.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

@app.get("/")
async def root():
    return {"message": "Hello Morpheus"}

@app.get("/healthCheck")
async def health_check():
    return {"message": "Service is up!"}
