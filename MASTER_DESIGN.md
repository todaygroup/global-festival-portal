# 🌐 Festa Guide: Master Enterprise Architecture (v1.0)

## 📌 1. Project Identity
- **Project Name**: Festa Guide
- **Domain**: festaguide.com
- **Core Concept**: [Raw Data $\rightarrow$ High-Fi Knowledge $\rightarrow$ Multimodal Content $\rightarrow$ Global Distribution]
- **Vision**: 전 세계 모든 축제를 '결정-계획-방문'까지 한 번에 해결하는 초고정밀 인텔리전스 포털 구축.
- **Core Principle**: **Zero Mock Policy** (모든 데이터는 물리적 근거 URL이 존재해야 하며, 허구의 데이터는 즉시 제거한다.)

---

## ⚙️ 2. Full-Stack Technical Architecture

### 2.1 Tech Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Zustand, React Query.
- **Backend**: FastAPI (Python 3.11+), Pydantic (Data Validation).
- **Database**: PostgreSQL + PostGIS (Geospatial Query), Redis (Caching).
- **AI Engine**: GPT-4o / Claude 3.5 (Data Enrichment & Scripting), Custom Agent Swarms.
- **Infra**: Vercel (Frontend), Docker (Backend), GitHub Actions (CI/CD).

### 2.2 Data Pipeline (The Intelligence Flow)
**[L1: Raw Lake] $\rightarrow$ [L2: Truth Lake] $\rightarrow$ [L3: Context Lake] $\rightarrow$ [Master DB]**
1. **L1 (Raw)**: `raw_content/` - 원천 HTML/JSON/텍스트 적재.
2. **L2 (Truth)**: `verified/` - Zero-Mock 검증 및 중복 제거 완료 데이터.
3. **L3 (Context)**: `enriched/` - SDS v2.0 규격(결정적 정보 10종) 적용 데이터.
4. **Master DB**: `festivals_master.json` / PostgreSQL - 최종 서비스 서빙용 통합 DB.

---

## 🤖 3. AI Orchestration Swarm System

### 3.1 Organization Chart
- **Chief Orchestrator**: 전체 태스크 배분 및 상태 모니터링 (`orchestrator.py`).
- **Intelligence Division**: 
    - `Hunter Agent`: 데이터 발굴 및 수집.
    - `Verifier Agent`: 무결성 검증 및 Mock 제거.
    - `Enricher Agent`: SDS v2.0 심층 정보 보강.
- **Knowledge Division**: 
    - `Wiki Architect`: 내부 지식 베이스 구조화.
    - `Storyteller`: 플랫폼별 맞춤형 스크립트/스토리 생성.
- **Creative Division**: 
    - `Media Prod Agent`: AI 영상/이미지 자동 생성.
- **Distribution Division**: 
    - `API Agent`: SNS(YouTube, TikTok, Insta) 자동 배포.

---

## 🗺️ 4. Service Blueprint & User Experience

### 4.1 Sitemap & Core Menus
- **Home**: AI 추천 큐레이션, 글로벌 축제 트렌드.
- **Explore (World Map)**: 
    - 동적 POI 맵핑 (Temporal Mapping).
    - 국가/시즌/테마별 정밀 필터링.
- **Festival Detail (High-Fidelity Page)**:
    - **Identity**: 공식 정보, 역사.
    - **Temporal**: 상세 일정 (Calendar View).
    - **Logistics**: 교통, 숙박 추천, 비자/입국 가이드.
    - **Experience**: TOP 3 하이라이트, 현지인 팁.
    - **Multimedia**: 공식/AI 생성 가이드 영상 및 갤러리.
- **My Planner**: 맞춤형 축제 루트 설계 및 저장.

### 4.2 User Journey Map
`Landing` $\rightarrow$ `Discovery (Map/Search)` $\rightarrow$ `Deep Dive (Detail Page)` $\rightarrow$ `Planning (My Planner)` $\rightarrow$ `Share/Visit`.

---

## 💰 5. Business & Growth Strategy

### 5.1 Monetization Model
- **B2C**: 프리미엄 가이드북(PDF) 판매, 맞춤형 일정 설계 구독 서비스.
- **B2B**: 축제 공식 파트너십 광고, 지역 상권(숙박/교통) 예약 API 연동 수수료.
- **Ads**: 고정밀 타겟팅 기반의 네이티브 광고 배치.

### 5.2 Expansion Strategy
- **PWA (Progressive Web App)**: 앱 설치 없이 모바일 네이티브 경험 제공.
- **Native App**: 위치 기반 실시간 푸시 알림 기능을 갖춘 iOS/Android 앱 확장.

---

## 🛠️ 6. Operational Governance

### 6.1 Quality Assurance (QA)
- **Zero-Mock Guard**: 모든 레코드는 `source_url`이 유효해야 하며, 정기적으로 URL 유효성을 전수 조사함.
- **Lifecycle Management**: 축제 종료 후 `Analysis` 단계로 전환하여 데이터를 아카이빙하고 차년도 예측 데이터로 업데이트.

### 6.2 Error & Maintenance
- **Sentry/Logging**: API 및 데이터 파이프라인 에러 실시간 모니터링.
- **Auto-Update Loop**: 공식 사이트 변경 감지 시 자동으로 `L1` 수집부터 `Master DB`까지 업데이트 트리거 작동.

---

## 📂 7. Physical Resource Mapping (Workspace)

| 설계 구성 요소 | 물리적 파일/경로 | 상태 |
| :--- | :--- | :---: |
| **Raw Data Lake** | `/home/aiagent/hyeongryeol_workspace/raw_content/` | 🟢 확보 |
| **Data Enrichment** | `/home/aiagent/hyeongryeol_workspace/enrich_data.py` | 🟡 준비 |
| **Master DB** | `/home/aiagent/hyeongryeol_workspace/festivals_master.json` | 🔴 비어있음 |
| **Intelligence Lake** | `/home/aiagent/hyeongryeol_workspace/festa_global_db/` | 🟡 일부생성 |
| **Master Design** | `/home/aiagent/hyeongryeol_workspace/MASTER_DESIGN.md` | 🟢 최신화 |
