# Facade 패턴 - 홈시어터 예제

## 목적

복잡한 서브시스템(앰프, DVD 플레이어, 프로젝터, 조명, 스크린, 팝콘 기계)을
`HomeTheaterFacade` 하나로 감싸, 클라이언트가 `watch_movie()` / `end_movie()`
두 메서드만으로 전체 흐름을 제어하게 한다.

## 설계

### 서브시스템

각 서브시스템은 공유 이벤트 로그(`log: list[str]`)를 주입받고, 동작할 때마다
로그에 문자열을 남긴다. Facade가 호출 순서를 제대로 조율하는지 테스트로 검증하기 위함.
서브시스템은 Facade의 존재를 전혀 모른다 (단방향 의존).

| 클래스 | 메서드 | 로그 예시 |
|--------|--------|-----------|
| `Amplifier` | `on()`, `off()`, `set_dvd(dvd)`, `set_volume(level)` | `"amp on"`, `"amp volume 5"` |
| `DvdPlayer` | `on()`, `off()`, `play(movie)`, `stop()`, `eject()` | `"dvd play 인터스텔라"` |
| `Projector` | `on()`, `off()`, `wide_screen_mode()` | `"projector wide_screen"` |
| `TheaterLights` | `on()`, `dim(level)` | `"lights dim 10"` |
| `Screen` | `up()`, `down()` | `"screen down"` |
| `PopcornPopper` | `on()`, `off()`, `pop()` | `"popper pop"` |

### Facade

```
HomeTheaterFacade(amp, dvd, projector, lights, screen, popper)
```

- `watch_movie(movie)` 순서:
  1. `popper.on()` → `popper.pop()`
  2. `lights.dim(10)`
  3. `screen.down()`
  4. `projector.on()` → `projector.wide_screen_mode()`
  5. `amp.on()` → `amp.set_dvd(dvd)` → `amp.set_volume(5)`
  6. `dvd.on()` → `dvd.play(movie)`

- `end_movie()` 순서 (대략 역순):
  1. `popper.off()`
  2. `lights.on()`
  3. `screen.up()`
  4. `projector.off()`
  5. `amp.off()`
  6. `dvd.stop()` → `dvd.eject()` → `dvd.off()`

### 원칙

- Facade는 조합·위임만 한다. 비즈니스 로직 없음.
- 서브시스템은 독립적으로도 직접 사용 가능해야 한다.
- Facade는 서브시스템 직접 접근을 막지 않는다 (강제 아님, 편의).

## 파일 구조

```
conftest.py                        # 빈 파일, repo 루트를 import 경로에 추가
facade/home_theater.py             # 서브시스템 + Facade
tests/facade/test_home_theater.py
```

## TDD 계획 (red → green → refactor)

1. **RED**: `watch_movie("인터스텔라")` 호출 후 로그가 기대 순서와 일치하는지 검증하는 테스트. 아직 클래스 없어 import 실패 → red.
2. **GREEN**: 서브시스템 6개 + Facade 최소 구현. 테스트 통과.
3. **RED**: `end_movie()` 로그 순서 테스트 추가.
4. **GREEN**: `end_movie()` 구현.
5. **RED**: 서브시스템 독립 사용 테스트 (`Amplifier` 하나만 켜고 로그 확인).
6. **REFACTOR**: 중복 정리, 이름 다듬기.

## 결과 (2026-09-07 완료)

- `facade/home_theater.py`: 서브시스템 6개 + `Device` base + `HomeTheaterFacade`
- `tests/facade/test_home_theater.py`: 4 passed
  1. `watch_movie` 위임 순서 검증
  2. `end_movie` 위임 순서 검증
  3. 서브시스템 단독 사용 (Facade 없이 동작)
  4. Facade 매크로 실행 후 서브시스템 직접 접근 (`facade.amp.set_volume(11)`)
- refactor: 서브시스템 공통 `__init__`을 `Device` base로 추출

### 배운 점

- 서브시스템 간 결합(`Amplifier.set_dvd`)은 도메인 고유의 것. Facade가 없애는 건 그게 아니라 "클라이언트가 배선을 직접 하는 상황".
- 서브시스템 → Facade 방향 의존은 없어야 함 (단독 사용 가능해야 함).
- Facade는 public 접근을 막지 않는다. 편의지 강제가 아니다.
- Adapter(인터페이스 변환) / Mediator(양방향 조정)와 구분.

## 확장 아이디어 (나중에)

- `listen_to_radio()` 같은 다른 시나리오 추가 → Facade가 여러 "매크로" 제공
- 서브시스템을 실제 하드웨어 드라이버로 교체해도 Facade 인터페이스 불변인지 확인
