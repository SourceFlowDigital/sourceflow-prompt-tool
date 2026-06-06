from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.config import settings
from routers import auth, prompt, quota

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth.router, prefix="/api/auth")
app.include_router(auth.me_router, prefix="/api")
app.include_router(prompt.router, prefix="/api/prompt")
app.include_router(quota.router, prefix="/api/quota")


@app.get("/health")
def health_check():
    return {"status": "ok", "version": settings.VERSION}
