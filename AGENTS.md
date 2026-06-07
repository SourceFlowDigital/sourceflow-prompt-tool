# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

**源流AI提示词工具** (SourceFlow AI Prompt Tool): a uni-app (Vue 3) frontend plus FastAPI backend for generating structured AI prompts via a 4-step wizard (scene → role → identity → task). The **basic mode runs entirely client-side** today; the backend exposes `/health` and `POST /api/prompt/build` (MySQL-backed).

### Services

| Service | Directory | Start command | Port |
|---------|-----------|---------------|------|
| Frontend (H5) | `frontend/` | `npm run dev:h5` | 5173 |
| Backend API | `backend/` | `. .venv/bin/activate && uvicorn app.main:app --reload --port 8003` | 8003 |
| MySQL 8 | system | `sudo service mysql start` | 3306 |

Use **tmux** for long-running dev servers (see cloud agent setup notes).

### Backend prerequisites

1. **Python venv**: Ubuntu images may need `sudo apt-get install -y python3.12-venv` once before `python3 -m venv backend/.venv`.
2. **MySQL**: Backend import fails without a valid `DATABASE_URL`. Copy `backend/.env.example` to `backend/.env`, ensure MySQL is running, create DB/user, and apply `backend/database/init.sql`. The `agent_templates` table is **not** in `init.sql`; seed it separately for `/api/prompt/build` to return roles (see status report references to `agent_templates_insert.sql`).
3. **Local dev DB** (example): database `sourceflow_prompt`, user `sourceflow` / `sourceflow_dev`, URL `mysql+pymysql://sourceflow:sourceflow_dev@localhost:3306/sourceflow_prompt`.

### Lint / test

This repo has **no** root lint scripts, pre-commit hooks, or automated test suites. Verification commands:

- Frontend build: `cd frontend && npm run build:h5`
- Backend health: `curl http://localhost:8003/health`
- Backend prompt API (needs seeded `agent_templates`): `curl -X POST http://localhost:8003/api/prompt/build -H "Content-Type: application/json" -d '{"role_id":"growth-hacker","user_input":"test"}'`

### Frontend-only E2E

For UI wizard testing, only the frontend dev server is required. Open `http://localhost:5173/` and complete the four steps; prompt generation and copy use static `categories.js` / `roles.js` data.

### Docs

- Backend setup: `backend/README.md`
- Project status / SQL notes: `项目状态报告_2026-06-07_Codex-SCENE-SQL01.md`
