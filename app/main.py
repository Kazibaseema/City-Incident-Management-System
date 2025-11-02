from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="City Incident Microservice")

app.include_router(router)
