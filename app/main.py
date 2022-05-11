from fastapi import FastAPI

from .routers import user_data

app = FastAPI()

app.include_router(user_data.router)


@app.get("/")
async def root():
    return {"message": "Hello Morpheus"}

@app.get("/healthCheck")
async def health_check():
    return {"message": "Service is Up!"}
