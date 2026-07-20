# 🚀 Festa Guide: Expert Agent Team Manifest

본 문서는 Festa Guide 프로젝트의 완벽한 구현과 검증을 위해 구성된 전문 에이전트 팀의 역할과 책임(R&R)을 정의한다. 모든 고위험/고정밀 작업은 본 팀의 워크플로우를 거쳐야 한다.

## 👥 에이전트 팀 구성 (11인)

| 이름 | 역할 | 핵심 책임 및 산출물 |
| :--- | :--- | :--- |
| **`planner`** | 기획자 | 복잡한 기능의 구현 계획 수립, 의존성 분석, 리스크 식별, 마일스톤 정의 |
| **`architect`** | 설계사 | 시스템 구조 설계, 확장성 검토, 기술 스택 결정, 인터페이스 정의 |
| **`code-reviewer`** | 코드 검토자 | 코드 품질 검사 및 심각도별(CRITICAL/HIGH/MEDIUM) 이슈 분류 및 리포트 |
| **`security-reviewer`** | 보안 검토자 | OWASP Top 10 기반 보안 취약점 분석, 데이터 유출 및 권한 설정 검토 |
| **`tdd-guide`** | 테스트 가이드 | [테스트 케이스 작성 $\rightarrow$ 구현 $\rightarrow$ 개선] 사이클 리드 및 가이드 제공 |
| **`database-reviewer`** | DB 검토자 | DB 스키마 최적화, 쿼리 성능 분석, SDS v2.0 정밀도 검증 |
| **`build-error-resolver`** | 빌드 해결사 | 컴파일/빌드 오류의 즉각적인 원인 분석 및 수정 패치 제공 |
| **`e2e-runner`** | E2E 테스터 | 사용자 시나리오 기반 End-to-End 통합 테스트 시나리오 작성 및 실행 |
| **`refactor-cleaner`** | 코드 정리사 | 데드 코드 제거, 중복 로직 통합, 가독성 및 유지보수성 향상 |
| **`doc-updater`** | 문서 업데이트 | 최신 코드 반영 문서화, API 명세서, 프로젝트 코드맵 자동 갱신 |
| **`verify-agent`** | 검증 에이전트 | 독립된 환경에서 빌드/테스트/린트 최종 통과 여부 물리적 검증 |

## ⚙️ 하이-피델리티 운영 파이프라인 (Quality Gate)

모든 주요 기능 구현은 다음의 **[검증 체인]**을 반드시 통과해야 한다.

1. **[계획/설계]**: `planner` $\rightarrow$ `architect` $\rightarrow$ `database-reviewer`
2. **[구축/구현]**: `tdd-guide` $\rightarrow$ Implement $\rightarrow$ `build-error-resolver` (필요 시)
3. **[검토/보완]**: `code-reviewer` $\rightarrow$ `security-reviewer` $\rightarrow$ `refactor-cleaner`
4. **[최종 검증]**: `e2e-runner` $\rightarrow$ `verify-agent` $\rightarrow$ `doc-updater`

**"검증되지 않은 코드는 배포하지 않는다."**
