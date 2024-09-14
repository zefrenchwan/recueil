from fastapi import APIRouter

checks_router = APIRouter()

@checks_router.get("/status")
async def status():
    return {"status": "RUNNING"}