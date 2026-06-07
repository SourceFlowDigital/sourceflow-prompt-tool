from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/api/prompt", tags=["prompt"])


class BuildRequest(BaseModel):
    role_id: str
    user_input: str
    language: str = "zh"  # zh=中文模板 en=英文模板


class BuildResponse(BaseModel):
    role_id: str
    role_name: str
    prompt: str
    mode: str = "basic"


@router.post("/build", response_model=BuildResponse)
async def build_prompt(req: BuildRequest, db: Session = Depends(get_db)):
    # 1. 参数校验
    if not req.role_id or not req.user_input.strip():
        raise HTTPException(status_code=400, detail="role_id和user_input不能为空")
    if len(req.user_input) > 500:
        raise HTTPException(status_code=400, detail="user_input不能超过500字")

    # 2. 查询角色模板
    result = db.execute(
        text(
            """
            SELECT name_zh, name_en, prompt_template_zh, prompt_template_en,
                   core_mission_zh, vibe_zh
            FROM agent_templates
            WHERE role_id = :role_id AND is_active = 1
            """
        ),
        {"role_id": req.role_id},
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail=f"角色不存在：{req.role_id}")

    # 3. 选择模板语言
    if req.language == "zh":
        template = result.prompt_template_zh or result.prompt_template_en or ""
        role_name = result.name_zh
        mission = result.core_mission_zh or ""
        vibe = result.vibe_zh or ""
    else:
        template = result.prompt_template_en or ""
        role_name = result.name_en
        mission = ""
        vibe = ""

    # 4. 拼装结构化提示词
    prompt = f"""# AI角色提示词

## 角色设定
你现在扮演：{role_name}
{f'角色特质：{vibe}' if vibe else ''}

## 核心职责
{mission}

## 工作方式
{template}

## 你的任务
{req.user_input.strip()}

---
请以{role_name}的身份，按照以上工作方式，完成上述任务。"""

    return BuildResponse(
        role_id=req.role_id,
        role_name=role_name,
        prompt=prompt.strip(),
        mode="basic",
    )
