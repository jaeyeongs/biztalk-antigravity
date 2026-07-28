import os
import sys

# sys.path 설정 (Vercel 서벌리스 모듈 임포트 방어)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import convert
from models.schemas import HealthCheckResponse

app = FastAPI(
    title="업무 말투 변환기 API",
    description="Upstage Solar-Pro 모델 기반 업무 말투 변환 백엔드 서비스",
    version="1.0.0"
)

# CORS 설정 (전면 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(convert.router, prefix="/api", tags=["Convert"])

# Health Check 엔드포인트
@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    return HealthCheckResponse(status="ok")

# 프론트엔드 정적 파일 및 메인 페이지 라우팅
frontend_dir = os.path.abspath(os.path.join(current_dir, "..", "frontend"))
if os.path.exists(frontend_dir):
    css_dir = os.path.join(frontend_dir, "css")
    js_dir = os.path.join(frontend_dir, "js")
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")

    @app.get("/")
    async def serve_index():
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "업무 말투 변환기 백엔드 서버가 작동 중입니다."}
