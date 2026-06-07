"""Smoke tests for POST /api/prompt/optimize (no real API key required)."""

import os
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))
os.environ.setdefault("DEEPSEEK_API_KEY", "")

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)


def test_optimize_empty_base_prompt():
    response = client.post("/api/prompt/optimize", json={"base_prompt": "   "})
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert data["error"] == "基础提示词不能为空"


def test_optimize_missing_api_key():
    settings.DEEPSEEK_API_KEY = ""
    response = client.post(
        "/api/prompt/optimize",
        json={"base_prompt": "你是一名内容创作者。你的任务是：写一段产品介绍。"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert data["error"] == "AI 优化服务暂不可用，请稍后再试"


def test_optimize_too_long_base_prompt():
    response = client.post(
        "/api/prompt/optimize",
        json={"base_prompt": "x" * 6001},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert data["error"] == "提示词内容过长，请缩短后再试"


if __name__ == "__main__":
    test_optimize_empty_base_prompt()
    print("PASS: empty base_prompt")
    test_optimize_missing_api_key()
    print("PASS: missing API key")
    test_optimize_too_long_base_prompt()
    print("PASS: too long base_prompt")
    print("All optimize smoke tests passed.")
