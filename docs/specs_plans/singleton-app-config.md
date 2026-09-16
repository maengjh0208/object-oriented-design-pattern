# Singleton — 앱 설정 관리자

- 분류: 생성 (Creational)
- 예제: 앱 설정 관리자 (AppConfig)
- 구현 위치: `creational/singleton/`, 테스트 `tests/creational/singleton/`

---

## 1. 스펙

### 목표

앱 전체가 공유하는 설정값(디버그 모드, API 키 등)을 인스턴스 하나로만 존재하게 강제한다.
어디서 `AppConfig()`를 부르든 같은 객체를 받고, 한쪽에서 바꾼 값이 다른 쪽에서도 보인다.

### 등장 요소

| 역할 | 이름 | 책임 |
|------|------|------|
| Singleton 클래스 | `AppConfig` | `__new__` 오버라이드로 인스턴스 하나만 존재하도록 강제 |
| 클래스 변수 | `_instance` | 캐싱된 유일 인스턴스 저장 |
| 인스턴스 변수 | `_initialized` | `__init__` 재실행 방지 가드 |
| 속성 | `debug`, `api_key` | 설정값 (기본값 `False`, `None`) |

### 동작 규칙

- `AppConfig()`를 몇 번 부르든 같은 객체(`is` 비교 참) 반환.
- `__new__`가 첫 호출에서만 실제 객체를 만들고, 이후엔 `_instance`에 캐싱된 걸 반환.
- `__init__`은 `__new__`가 뭘 반환하든 인스턴스일 때마다 다시 불림 — 이걸 그냥 두면
  기존 상태가 매번 기본값으로 덮어써짐. `_initialized` 플래그로 최초 1회만 초기화.

---

## 2. TDD 계획

red → green. 한 번에 테스트 하나.

| # | 실패 테스트 | 통과시키는 최소 구현 |
|---|-------------|----------------------|
| 1 | `AppConfig() is AppConfig()` → `True` | `AppConfig.__new__`에서 `_instance` 캐싱 |
| 2 | 새 `AppConfig()`의 `debug is False`, `api_key is None` | `__init__`에서 기본값 설정 |
| 3 | `config.debug = True` 후 `AppConfig()` 다시 호출해도 `config.debug is True` 유지 | `__init__`에 `hasattr(self, "_initialized")` 가드 추가 |

---

## 3. 결과 / 배운 점

### 최종 구조

```
creational/singleton/
  app_config.py   # AppConfig — __new__ 로 인스턴스 캐싱, __init__ 은 최초 1회만 동작
tests/creational/singleton/
  test_app_config.py   # 동일 인스턴스, 기본값, 상태 유지 검증
```

```python
class AppConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.debug = False
        self.api_key = None
        self._initialized = True
```

테스트 3개 통과.

### 배운 점

- **`__new__`와 `__init__`은 다른 책임.** `__new__`는 인스턴스를 만들지 말지 결정,
  `__init__`은 만들어진 인스턴스를 초기화. Singleton은 생성 자체를 통제해야 하니
  `__new__`를 손대야 한다 — `__init__`만 오버라이드해선 구현 불가능.
- **`__init__`은 매번 다시 불린다.** `AppConfig()`가 캐싱된 기존 인스턴스를 반환해도,
  반환값이 `AppConfig` 인스턴스인 이상 `__init__`은 재실행됨. 가드 없으면 기존 상태가
  기본값으로 덮어써진다. "인스턴스 하나"와 "상태가 유지된다"는 별개 문제.
- **`hasattr` 가드는 인스턴스 속성 기준.** `self._initialized`는 인스턴스 `__dict__`에
  박히는 것이라 첫 호출엔 없어서 `False`, 세팅 후엔 있어서 `True`. 클래스 변수로
  두면(`_instance`처럼) 인스턴스 생성 전부터 이미 존재해서 가드가 항상 통과해버리는
  버그가 생긴다.
- **`is` 비교로 정체성 검증.** `==`가 아니라 `is`를 써야 "같은 객체"를 확인한다.
  `__eq__` 오버라이드 안 했으면 결과는 같지만, 의도를 드러내려면 `is`.

### 한계 / 주의

- **테스트 간 상태 오염 (실제로 겪음).** `_instance`가 클래스 변수라 프로세스(테스트
  세션) 동안 안 사라진다. `test_mutated_state_survives_second_call`이 바꿔놓은
  `debug = True`가 그 뒤에 실행되는 다른 테스트에도 그대로 남는다. 지금은 테스트
  순서가 우연히 안 깨지게 짜여 있지만, 순서를 바꾸거나(`pytest-randomly` 등) 다른
  테스트 파일에서 `AppConfig()`를 먼저 건드리면 값이 새서 깨질 수 있다. 고치려면
  fixture에서 `AppConfig._instance = None`으로 매 테스트 리셋해야 하는데, 이건
  Singleton을 테스트하기 어렵다는 비판이 코드로 드러난 것 — 여기선 문제만 기록하고
  넘어간다.
- **스레드 세이프 아님.** 두 스레드가 동시에 `cls._instance is None`을 통과하면
  인스턴스가 두 개 생길 수 있다(레이스 컨디션). 이 예제는 단일 스레드 학습 목적이라
  lock 안 넣음. 필요해지면 `threading.Lock`으로 `__new__` 감싸는 게 표준 해법.
- **숨은 의존성.** `AppConfig()`는 아무 데서나 부를 수 있어서, 그걸 쓰는 함수의
  시그니처만 봐선 이 의존성이 안 보인다. 낮은 결합도 원칙과 정면으로 충돌하는 지점.
- **파이썬다운 대안.** 사실 파이썬에선 클래스 기반 Singleton보다 **모듈 레벨
  인스턴스**(`config = AppConfig()`를 모듈에 한 번 만들고 다들 import해서 씀)가
  더 단순하고 관용적이다. 모듈은 프로세스당 한 번만 로드되므로 자연히 싱글턴이 된다.
  이번 구현은 GoF 패턴 자체(`__new__` 오버라이드 메커니즘)를 배우려고 정석대로 간
  것 — 실무에서 새 설정 객체 만든다면 모듈 레벨 인스턴스부터 고려할 것.
