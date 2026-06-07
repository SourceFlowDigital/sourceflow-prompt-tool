import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是专业的 AI 提示词优化助手。用户会提供一条基础提示词及可选上下文。
请将其优化为更清晰、结构化、可直接复制使用的提示词正文。

要求：
1. 保留用户原始意图，不要替用户编造不存在的事实
2. 补全角色、目标、上下文、输出格式、约束、质量标准等必要要素
3. 让提示词更专业、完整，但仍聚焦任务本身
4. 只输出优化后的提示词正文，不要输出解释、标题说明、Markdown 代码块包装或前后缀说明
5. 使用中文输出（除非基础提示词主体为英文）"""


class DeepSeekError(Exception):
    """Raised when DeepSeek API call fails."""


def build_user_message(
    base_prompt: str,
    role_name: str | None = None,
    scenario: str | None = None,
    task: str | None = None,
) -> str:
    sections = [f"【基础提示词】\n{base_prompt.strip()}"]

    if role_name and role_name.strip():
        sections.append(f"【角色名称】\n{role_name.strip()}")
    if scenario and scenario.strip():
        sections.append(f"【应用场景】\n{scenario.strip()}")
    if task and task.strip():
        sections.append(f"【任务描述】\n{task.strip()}")

    sections.append("请直接输出优化后的提示词正文。")
    return "\n\n".join(sections)


def parse_usage(payload: dict[str, Any]) -> dict[str, int | None]:
    usage = payload.get("usage") or {}
    return {
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }


async def optimize_prompt(
    base_prompt: str,
    *,
    role_name: str | None = None,
    scenario: str | None = None,
    task: str | None = None,
) -> tuple[str, str, dict[str, int | None]]:
    api_key = settings.DEEPSEEK_API_KEY.strip()
    if not api_key:
        raise DeepSeekError("AI 优化服务暂不可用，请稍后再试")

    model = settings.DEEPSEEK_MODEL.strip() or "deepseek-chat"
    url = f"{settings.DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_message(
                    base_prompt,
                    role_name=role_name,
                    scenario=scenario,
                    task=task,
                ),
            },
        ],
        "temperature": settings.DEEPSEEK_TEMPERATURE,
        "max_tokens": settings.DEEPSEEK_MAX_TOKENS,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=settings.DEEPSEEK_TIMEOUT_SECONDS) as client:
            response = await client.post(url, headers=headers, json=body)
    except httpx.TimeoutException:
        logger.warning("DeepSeek request timed out")
        raise DeepSeekError("AI 优化服务暂不可用，请稍后再试") from None
    except httpx.HTTPError:
        logger.warning("DeepSeek network error", exc_info=True)
        raise DeepSeekError("AI 优化服务暂不可用，请稍后再试") from None

    if response.status_code != 200:
        logger.warning("DeepSeek HTTP error: status=%s", response.status_code)
        raise DeepSeekError("AI 优化服务暂不可用，请稍后再试")

    try:
        payload = response.json()
        choices = payload.get("choices") or []
        message = choices[0].get("message") if choices else None
        content = (message or {}).get("content", "")
        optimized = content.strip() if isinstance(content, str) else ""
    except (IndexError, KeyError, TypeError, ValueError):
        logger.warning("DeepSeek response parse error", exc_info=True)
        raise DeepSeekError("AI 优化服务暂不可用，请稍后再试") from None

    if not optimized:
        raise DeepSeekError("AI 优化服务暂不可用，请稍后再试")

    return optimized, payload.get("model") or model, parse_usage(payload)
