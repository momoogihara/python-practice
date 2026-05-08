from fastapi import FastAPI
from api import router as api_router
from api2 import router as api2_router
from api3 import router as api3_router

app = FastAPI()

app.include_router(api_router)
app.include_router(api2_router)
app.include_router(api3_router)