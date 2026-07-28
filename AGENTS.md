# AGENTS.md — Antigravity 개발 가이드라인 및 프로젝트 개요

이 문서는 **업무 말투 변환기(`biztalk-antigravity`)** 프로젝트를 개발할 때 Antigravity AI 에이전트가 준수해야 하는 규칙과 프로젝트 개요, 그리고 디렉토리 현황을 정의합니다.

---

## 1. 프로젝트 개요 (Project Overview)

- **프로젝트명**: 업무 말투 변환기 (`biztalk-antigravity`)
- **목적**: 사용자가 전달하고 싶은 메시지를 입력하고 수신 대상을 선택하면, AI(Upstage Solar-Pro3)를 통해 상황에 맞는 정중하고 적절한 비즈니스 언어로 자동 변환해주는 웹 서비스입니다.
- **개발 형태**: One Day 바이브 코딩 실습 프로젝트 ("작동하는 핵심 서비스"에 집중)
- **주요 기능**:
  - 텍스트 원문 입력 및 수신 대상 선택 (`boss`: 상사/임원, `colleague`: 타팀 동료, `client`: 고객/외부, `team`: 팀 내 동료)
  - FastAPI + LangChain + Upstage Solar-Pro3 연동 백엔드 API (`POST /api/convert`)
  - 변환 결과 화면 표시 및 클립보드 복사 기능
  - Health Check (`GET /health`) 및 Swagger API 문서 (`/docs`)
  - GitHub 및 Vercel 배포

---

## 2. 프로젝트 디렉토리 현황 및 목표 구조

### 📂 2-1. 현재 실제 디렉토리 현황 (Current Workspace)

STEP 1 (환경 준비)가 완료되어 기본 디렉토리 구조 및 백엔드 의존성이 구성되었습니다.

```text
biztalk_antigravity/
├── backend/                    # 백엔드 서버 디렉토리
│   ├── models/                 # Pydantic 모델 디렉토리 (__init__.py)
│   ├── prompts/                # 프롬프트 템플릿 디렉토리 (__init__.py)
│   ├── routers/                # API 라우터 디렉토리 (__init__.py)
│   ├── services/               # 비즈니스 로직 디렉토리 (__init__.py)
│   └── requirements.txt        # 백엔드 명시적 패키지 버전 목록
├── frontend/                   # 프론트엔드 웹 UI 디렉토리
│   ├── css/                    # 커스텀 스타일 디렉토리
│   └── js/                     # JS 스크립트 디렉토리
├── 개요서_업무말투변환기.md        # 서비스 기획 및 실습 개요서
├── PRD_업무말투변환기.md        # 제품 요구사항 명세서 (PRD)
├── AGENTS.md                   # Antigravity 개발 및 규칙 가이드라인 (본 문서)
├── README.md                   # 프로젝트 리드미 파일
├── pyproject.toml / uv.lock    # Python 프로젝트 및 uv 의존성 관리 파일
├── .python-version             # Python 버전 지정 파일 (3.12+)
├── .env                        # UPSTAGE_API_KEY 등 환경 변수 (Git 추적 제외)
├── .gitignore                  # Git 추적 제외 설정 (.env, .venv, __pycache__ 등)
├── test.py                     # Upstage Solar-Pro 연동 검증용 샘플 코드
└── .agents/                    # 에이전트 설정 파일 (mcp_config.json)
```

---

### 🎯 2-2. 구현 목표 디렉토리 구조 (Target Directory Structure)

구현 과정(STEP 1~3)에서 작성/구조화할 최종 디렉토리 목표입니다.

```text
biztalk_antigravity/
├── backend/                    # 백엔드 서버 디렉토리
│   ├── main.py                 # FastAPI 애플리케이션 및 CORS/라우팅 설정
│   ├── routers/
│   │   └── convert.py          # /api/convert API 라우터
│   ├── services/
│   │   └── tone_converter.py   # LangChain + Upstage Solar-Pro 연동 로직
│   ├── prompts/
│   │   └── templates.py        # 수신 대상별 프롬프트 템플릿
│   ├── models/
│   │   └── schemas.py          # Pydantic 요청/응답 데이터 모델
│   └── requirements.txt        # 의존성 패키지 목록
│
├── frontend/                   # 프론트엔드 웹 UI 디렉토리
│   ├── index.html              # 메인 UI 레이아웃
│   ├── css/
│   │   └── style.css           # 커스텀 UI 스타일
│   └── js/
│       └── app.js              # 이벤트 처리 및 백엔드 API 호출 스크립트
│
├── .env                        # 환경 변수 (UPSTAGE_API_KEY)
├── .gitignore                  # Git 제외 설정
├── pyproject.toml / uv.lock    # uv 패키지 매니저 파일
├── 개요서_업무말투변환기.md        # 서비스 기획 개요서
├── PRD_업무말투변환기.md        # 제품 요구사항 명세서
└── AGENTS.md                   # Antigravity 가이드라인
```

---

## 3. Antigravity 핵심 개발 규칙 (Rules for Antigravity)

### 🎯 규칙 1: 바이브 코딩 3원칙 엄격 준수

1. **완료 기준 먼저 정의 (기능 범위 고수)**
   - `PRD_업무말투변환기.md`에 명시된 완료 체크리스트 기능만 구현합니다.
   - 요청받지 않은 기능(로그인, 회원가입, DB 연동, 과도한 디자인 고도화 등)을 임의로 추가하거나 확장하지 않습니다.
2. **조사 먼저, 구현 나중**
   - 새로운 패키지나 API(Upstage Solar-Pro, LangChain 최신 버전 등)를 적용할 때는 구현 코드를 작성하기 전에 연동 방식과 인터페이스를 먼저 확인/조사합니다.
3. **버그는 분석 먼저, 수정 나중**
   - 에러가 발생한 경우 임의로 코드를 수정해 누더기를 만들지 말고, 로그 및 에러 메시지의 원인을 먼저 명확히 분석한 후 수정을 진행합니다.

---

### 🛠️ 규칙 2: 기술 스택 및 환경 지침

- **언어 및 패키지 관리**: Python 3.12+ / `uv` 매니저 사용
- **백엔드**: FastAPI, Uvicorn, LangChain, `langchain-upstage`, `python-dotenv`, Pydantic
- **프론트엔드**: Vanilla HTML5, CSS3, JavaScript (ES6+). 불필요한 프론트엔드 프레임워크(React, Vue 등) 도입 금지.
- **LLM 모델**: Upstage `solar-pro` (또는 `solar-pro3` API 명세 준수)

---

### 🔒 규칙 3: 보안 및 민감 정보 보호

- `.env` 파일에 `UPSTAGE_API_KEY`를 관리하고, `.env` 파일이나 API 키가 Git 커밋 및 외부 응답에 노출되지 않도록 엄격히 관리합니다.
- `.gitignore`에 `.env` 및 환경 관련 파일이 포함되어 있는지 확인합니다.

---

### ⚠️ 규칙 4: 코드 변경 및 Git 커밋 안전 원칙

- **파괴적 작업 금지**: `git push --force`, `git reset --hard`, `rm -rf` 등 파괴적 명령은 사용자 승인 없이 실행하지 않습니다.
- **단일 검증 원칙**: 코드를 변경하거나 추가한 후에는 서버 실행 및 동작 테스트를 수행하여 작동 여부를 확인합니다.

---

## 4. 실행 및 테스트 (Running & Testing)

### 4.1. 환경 설정
```bash
# uv를 사용한 가상환경 생성 및 의존성 설치
uv venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 4.2. 백엔드 실행
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4.3. 프론트엔드 확인
- `frontend/index.html`은 `http://localhost:8000` 으로 확인합니다. 
---

## 5. 보안 및 금지 사항 (Security & Restrictions)

- **API 키 보호**: `.env` 파일에 저장된 `UPSTAGE_API_KEY` 등이 코드에 노출되거나 커밋되지 않도록 주의합니다.
- **Git 조작**: Git 관련 금지 작업(강제 푸시, 히스토리 파괴 등)을 절대 수행하지 않습니다.
- **응답 언어**: 모든 설명과 주석은 **한국어**로 작성합니다.
---

### 6. @PRD_업무말투변환기.md 문서와 AGENTS.md 문서 항상 최신화 하기
* 모든 변경사항이 발생하면 (예를 들어 기능이나 요구사항이 변경 되거나, 화면명세가 변경되거나, Source Code가 변경 되거나 라이브러리 버전이 변경되면) 관련된 markdown 문서들도 반드시 업데이트 합니다. 
* 구현이 완료된 사항들은 `@PRD_업무말투변환기.md\2. 완료 체크리스트`에 모두 체크표시를 해서 완료 되었음을 반드시 표시하세요.
* `@PRD_업무말투변환기.md\8. 단계별 구현 순서` 에서도 단계별로 구현이 완료되면 체크표시를 해서 완료 되었음을 반드시 표시하세요.