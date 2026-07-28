import os
import sys

# sys.path 설정 (Vercel 서벌리스 환경 모듈 임포트 방어)
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import APIRouter, HTTPException
from models.schemas import ConvertRequest, ConvertResponse
from services.tone_converter import tone_converter_service

router = APIRouter()

VALID_AUDIENCES = {"boss", "colleague", "client", "team"}

@router.post("/convert", response_model=ConvertResponse, summary="업무 말투 변환 API")
async def convert_text(request: ConvertRequest):
    """
    원문 텍스트와 수신 대상을 받아 비즈니스 어조로 변환합니다.
    - **text**: 변환할 원문
    - **target_audience**: boss(상사), colleague(타팀 동료), client(고객), team(팀 내 동료)
    """
    if request.target_audience not in VALID_AUDIENCES:
        raise HTTPException(
            status_code=422,
            detail=f"유효하지 않은 target_audience입니다. 허용값: {', '.join(VALID_AUDIENCES)}"
        )
    
    converted_result = tone_converter_service.convert_tone(
        text=request.text,
        target_audience=request.target_audience
    )

    return ConvertResponse(
        converted_text=converted_result,
        target_audience=request.target_audience,
        original_text=request.text
    )
