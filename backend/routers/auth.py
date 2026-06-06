from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
me_router = APIRouter()


class WechatLoginRequest(BaseModel):
    code: str


class GuestRequest(BaseModel):
    device_id: str


@router.post("/wechat-login")
def wechat_login(request: WechatLoginRequest):
    return {"message": "wechat-login placeholder"}


@router.post("/guest")
def guest_login(request: GuestRequest):
    return {"message": "guest placeholder"}


@me_router.get("/me")
def get_me():
    return {"message": "me placeholder"}
