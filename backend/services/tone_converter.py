import os
import sys
from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate

# sys.path 설정 (Vercel 서벌리스 모듈 임포트 호환)
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from prompts.templates import get_prompt_by_target

load_dotenv()

class ToneConverterService:
    def convert_tone(self, text: str, target_audience: str) -> str:
        """
        원문 텍스트와 수신 대상을 받아 Upstage Solar-Pro 모델로 말투를 변환합니다.
        """
        api_key = os.getenv("UPSTAGE_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="UPSTAGE_API_KEY가 설정되지 않았습니다. Vercel Environment Variables에 UPSTAGE_API_KEY를 추가해주세요."
            )
        
        try:
            llm = ChatUpstage(
                api_key=api_key,
                model="solar-pro",
                temperature=0.3
            )
            system_prompt = get_prompt_by_target(target_audience)
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "다음 원문을 적절한 비즈니스 말투로 변환해주세요:\n\n{text}")
            ])

            chain = prompt_template | llm
            response = chain.invoke({"text": text})
            
            return str(response.content).strip()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"LLM API 호출 중 오류가 발생했습니다: {str(e)}"
            )

tone_converter_service = ToneConverterService()
