from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def get_quota_status():
    return {"message": "quota status placeholder"}
