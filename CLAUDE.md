# CLAUDE.md

이 레포에서 Claude가 일하는 방식.

- 작업 시작 전 `PROJECT.md`를 읽는다.
- **코드는 사용자가 직접 타이핑한다.** Claude는 코드 파일(`<패턴>/*.py`, `tests/**`)을 대신 작성하지 않는다.
- Claude의 역할: 패턴 설명, TDD 단계별 스펙 제공(테스트/구현 명세), 사용자가 친 코드 리뷰(문법·오타·설계).
- 문서(`docs/`, `PROJECT.md`, `README.md`), 설정(`pyproject.toml`, `.gitignore`, `conftest.py`)은 Claude가 작성해도 된다.
- 각 패턴은 `docs/specs_plans/<패턴>.md`에 스펙 → TDD 계획 → 결과/배운 점 순으로 기록한다.
- 패턴 학습 순서: 사용자가 지정한다.
