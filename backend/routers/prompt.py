from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from services.deepseek import DeepSeekError, optimize_prompt

router = APIRouter(prefix="/api/prompt", tags=["prompt"])

MAX_BASE_PROMPT_LENGTH = 6000


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


class OptimizeRequest(BaseModel):
    base_prompt: str
    role_name: str | None = None
    scenario: str | None = None
    task: str | None = None


class UsageInfo(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class OptimizeSuccessResponse(BaseModel):
    ok: Literal[True] = True
    mode: Literal["advanced"] = "advanced"
    optimized_prompt: str
    provider: Literal["deepseek"] = "deepseek"
    model: str
    usage: UsageInfo


class OptimizeErrorResponse(BaseModel):
    ok: Literal[False] = False
    error: str


@router.post(
    "/optimize",
    response_model=OptimizeSuccessResponse | OptimizeErrorResponse,
)
async def optimize_prompt_endpoint(req: OptimizeRequest):
    base_prompt = req.base_prompt.strip()
    if not base_prompt:
        return OptimizeErrorResponse(error="基础提示词不能为空")
    if len(base_prompt) > MAX_BASE_PROMPT_LENGTH:
        return OptimizeErrorResponse(error="提示词内容过长，请缩短后再试")

    try:
        optimized_prompt, model, usage = await optimize_prompt(
            base_prompt,
            role_name=req.role_name,
            scenario=req.scenario,
            task=req.task,
        )
    except DeepSeekError as exc:
        return OptimizeErrorResponse(error=str(exc))

    return OptimizeSuccessResponse(
        optimized_prompt=optimized_prompt,
        model=model,
        usage=UsageInfo(**usage),
    )
