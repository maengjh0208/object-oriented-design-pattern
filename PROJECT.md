# PROJECT

객체지향 디자인 패턴을 직접 구현하며 공부하는 레포. 생성/구조/행동 패턴을 하나씩 다룬다.

## 구조

```
creational/<패턴>/     # 생성 패턴 구현 패키지
structural/<패턴>/     # 구조 패턴 구현 패키지 (예: structural/facade/)
behavioral/<패턴>/     # 행동 패턴 구현 패키지
tests/<분류>/<패턴>/   # 패턴별 테스트 (분류 = creational/structural/behavioral)
docs/specs_plans/      # 패턴별 스펙 + TDD 계획 문서
conftest.py            # 빈 파일, repo 루트를 import 경로에 추가
```

## 환경

- Python >= 3.12, 패키지 관리: `uv`
- `pyproject.toml`에 `[tool.uv] package = false` — 빌드 대상 아님, 코드 모음일 뿐
- 개발 의존성: `pytest`, `ruff`

## 명령

| 목적 | 명령 |
|------|------|
| 의존성 동기화 | `uv sync` |
| 전체 테스트 | `uv run pytest -q` |
| 특정 패턴 | `uv run pytest tests/structural/facade/ -q` |
| print 출력 보기 | `uv run pytest -s` |
| 린트 | `uv run ruff check` |

## 작업 방식

- TDD: red → green → refactor. 테스트가 스펙 역할.
- 각 패턴은 `docs/specs_plans/<패턴>.md`에 스펙·계획·결과를 남긴다.
- 코드는 사용자가 직접 타이핑한다. Claude는 스펙 제공·리뷰·설명 담당.

## 완료된 패턴

| 패턴 | 분류 | 예제 | 문서 |
|------|------|------|------|
| Facade | 구조 | 홈시어터 | `docs/specs_plans/facade-home-theater.md` |
| Strategy | 행동 | 장바구니 할인 정책 | `docs/specs_plans/strategy-discount-policy.md` |
| Template Method | 행동 | 음료 제조 (커피/홍차) | `docs/specs_plans/template-method-beverage.md` |
