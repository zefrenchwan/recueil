from fastapi import FastAPI
from checks import checks_router

app = FastAPI()

app.include_router(checks_router)