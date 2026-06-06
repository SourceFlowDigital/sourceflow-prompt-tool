from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PromptRequest(BaseModel):
    category_id: str
    role_id: str
    task: str


@router.post("/build")
def build_prompt(request: PromptRequest):
    return {"message": "prompt build placeholder"}


@router.post("/generate")
def generate_prompt(request: PromptRequest):
    return {"message": "prompt generate placeholder"}
