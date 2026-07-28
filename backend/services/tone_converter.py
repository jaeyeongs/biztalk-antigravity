import os
from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from prompts.templates import get_prompt_by_target

# 환경 변수 로드 (.env)
load_dotenv()

class ToneConverterService:
    def __init__(self):
        api_key = os.getenv("UPSTAGE_API_KEY")
        if not api_key:
            raise ValueError("UPSTAGE_API_KEY가 .env 파일에 설정되어 있지 않습니다.")
        
        self.llm = ChatUpstage(
            api_key=api_key,
            model="solar-pro",
            temperature=0.3
        )

    def convert_tone(self, text: str, target_audience: str) -> str:
        """
        원문 텍스트와 수신 대상을 받아 Upstage Solar-Pro 모델로 말투를 변환합니다.
        """
        try:
            system_prompt = get_prompt_by_target(target_audience)
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "다음 원문을 적절한 비즈니스 말투로 변환해주세요:\n\n{text}")
            ])

            chain = prompt_template | self.llm
            response = chain.invoke({"text": text})
            
            return response.content.strip()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"LLM API 호출 중 오류가 발생했습니다: {str(e)}"
            )

tone_converter_service = ToneConverterService()
