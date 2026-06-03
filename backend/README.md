# 源流AI提示词工具 API

源流AI提示词工具后端 FastAPI 服务骨架。

## 环境要求

Python 3.10+

## 安装步骤

```bash
pip install -r requirements.txt
```

## 启动命令

```bash
uvicorn app.main:app --reload --port 8003
```

## 健康检查

```bash
curl http://localhost:8003/health
```
