# Template Method — 음료 제조

- 분류: 행동 (Behavioral)
- 예제: 음료 제조 (커피 / 홍차)
- 구현 위치: `behavioral/template_method/`, 테스트 `tests/behavioral/template_method/`

---

## 1. 스펙

### 목표

음료를 만드는 **알고리즘 골격**(물 끓이기 → 우리기 → 따르기 → 첨가물)을 부모 클래스에
고정한다. 음료마다 달라지는 단계(우리는 법, 첨가물)만 서브클래스가 채운다.
공통 흐름은 한 곳에만 존재한다 (DRY).

### 등장 요소

| 역할 | 이름 | 책임 |
|------|------|------|
| AbstractClass | `Beverage` (ABC) | 템플릿 메서드 + 공통 단계 + 추상 단계 선언 |
| 템플릿 메서드 | `prepare()` | `boil_water` → `brew` → `pour_in_cup` → (훅이 참이면) `add_condiments` 순서로 호출. 오버라이드하지 않는다 |
| 공통 단계 | `boil_water()` | `steps` 에 `"물 끓이기"` append |
| 공통 단계 | `pour_in_cup()` | `steps` 에 `"컵에 따르기"` append |
| 추상 단계 | `brew()` | `@abstractmethod`. 자식이 구현 |
| 추상 단계 | `add_condiments()` | `@abstractmethod`. 자식이 구현 |
| 훅 | `wants_condiments()` | 기본 `return True`. 자식이 선택적으로 오버라이드 |
| ConcreteClass | `Coffee` | `brew` → `"커피 필터로 내리기"`, `add_condiments` → `"설탕과 우유 추가"` |
| ConcreteClass | `Tea` | `brew` → `"티백 우려내기"`, `add_condiments` → `"레몬 추가"` |

### 동작 규칙

- `Beverage.__init__` 이 `self.steps: list[str] = []` 초기화.
- 각 단계 메서드는 문자열 하나를 `self.steps` 에 append. 반환값 없음.
- `prepare()` 의 단계 순서는 고정. 서브클래스는 이 메서드를 건드리지 않는다.
- `wants_condiments()` 가 `False` 면 `prepare()` 는 `add_condiments()` 를 건너뛴다.
- `Beverage()` 직접 생성 → `TypeError` (추상 메서드 미구현). `brew` / `add_condiments`
  중 하나라도 안 채운 서브클래스도 인스턴스화 시 `TypeError`.
- 구조 제약: `Coffee` / `Tea` 는 `prepare` / `boil_water` / `pour_in_cup` 를 정의하지
  않는다. 공통 흐름은 부모만 소유한다 (의존·소유 방향 = 자식 → 부모 단방향).

### 훅 vs 추상 메서드

- **추상 메서드**(`brew`, `add_condiments`): 부모는 선언만. 자식이 **반드시** 구현. 안 하면 에러.
- **훅**(`wants_condiments`): 부모가 **무해한 기본 구현** 제공(`return True`). 자식이
  **원할 때만** 오버라이드. 알고리즘 골격에 자식이 선택적으로 개입하는 지점.

### 왜 상속인가 (vs Strategy)

| | Template Method | Strategy |
|--|--|--|
| 재사용 | 상속 (is-a) | 위임 (has-a) |
| 교체 시점 | 컴파일타임 (클래스 정의) | 런타임 |
| 바꾸는 범위 | 일부 단계만 | 알고리즘 전체 |
| 흐름 제어 | 부모가 자식 단계를 호출 (할리우드 원칙) | 클라이언트가 전략 주입 |

알고리즘 전체 순서가 항상 같고 **일부 단계만** 달라지면 Template Method.
알고리즘 전체를 런타임에 갈아끼워야 하면 Strategy.

---

## 2. TDD 계획

red → green → refactor. 한 번에 테스트 하나.

| # | 실패 테스트 | 통과시키는 최소 구현 |
|---|-------------|----------------------|
| 1 | `Coffee().prepare()` 후 `steps == ["물 끓이기", "커피 필터로 내리기", "컵에 따르기", "설탕과 우유 추가"]` | `Beverage` ABC + `prepare` 골격 + 공통 단계 + `Coffee` |
| 2 | `Tea().prepare()` 후 `steps == ["물 끓이기", "티백 우려내기", "컵에 따르기", "레몬 추가"]` | `Tea` 구현 |
| 3 | `Beverage()` → `TypeError` | `brew` / `add_condiments` 에 `@abstractmethod` (이미 됨, 검증만) |
| 4 | `wants_condiments()` → `False` 인 `BlackCoffee` → `prepare()` 후 `steps == ["물 끓이기", "커피 필터로 내리기", "컵에 따르기"]` | `prepare` 에 훅 분기 추가 + `wants_condiments` 기본 구현 |
| 5 | 구조: `"prepare" not in Coffee.__dict__`, `"boil_water" not in Coffee.__dict__` | (검증만, 구현 불필요) |

리팩터 포인트: 2번 통과 후 `prepare()` 의 단계 호출 나열을 정리. 훅 분기는 4번에서 추가.

---

## 3. 결과 / 배운 점

### 최종 구조

```
behavioral/template_method/
  beverage.py   # Beverage(ABC) — prepare() 템플릿 메서드, 공통 단계, 훅
                # Coffee, Tea (ConcreteClass), BlackCoffee (Coffee 변종, 훅만 오버라이드)
tests/behavioral/template_method/
  test_beverage.py   # 단계 순서, 훅 분기, 추상 클래스 차단, 구조 검증
```

테스트 5개 통과 (전체 스위트 17개 통과, ruff clean).

### 배운 점

- **템플릿 메서드가 흐름을 소유한다.** `prepare()` 가 `boil_water → brew → pour_in_cup
  → add_condiments` 순서를 고정한다. 서브클래스는 이 메서드를 오버라이드하지 않는다.
  `Coffee` / `Tea` 코드 = `brew()` + `add_condiments()` 두 개뿐. 변하는 부분만.
- **할리우드 원칙 (Don't call us, we'll call you).** 자식이 부모를 호출하는 게 아니라,
  부모 `prepare()` 가 자식이 채운 `brew()` 를 호출한다. 흐름 제어가 부모에 있다.
- **추상 메서드 vs 훅.**
  - `brew`, `add_condiments`: `@abstractmethod`. 자식이 반드시 구현. 안 하면 인스턴스화 시 `TypeError`.
  - `wants_condiments`: 훅. 부모가 기본 구현(`return True`) 제공. 자식이 원할 때만 오버라이드.
  - `BlackCoffee` 는 훅만 `False` 로 바꿨다. `add_condiments()` 는 (Coffee 에서 물려받아)
    여전히 존재하지만 `prepare()` 가 호출하지 않는다. **훅은 흐름을 제어하지 구현을 지우지 않는다.**
- **공통 흐름은 부모만 소유 (구조 테스트로 강제).** `"prepare" not in Coffee.__dict__`.
  `__dict__` 는 클래스에 직접 정의된 것만 담으므로, 자식이 `prepare` 를 재정의하면
  (= 패턴 위반) 테스트가 깨진다.
- **인스턴스 상태는 `__init__` 에서.** `self.steps = []` 를 클래스 변수로 두면 모든
  인스턴스가 공유해서 오염된다. `__init__` 에서 초기화해야 인스턴스마다 독립.
- **테스트하려고 `print` 를 `steps` 리스트로 바꿨다.** 원래 교과서 예제는 각 단계에서
  `print` 한다. 부작용을 리스트 append 로 바꾸니 `assert coffee.steps == [...]` 로
  순서·존재·생략을 한 번에 검증할 수 있다.
- **리팩터 단계가 "할 것 없음" 으로 끝났다.** `Coffee` / `Tea` 를 파라미터화하면
  (`Beverage(brew=..., cond=...)`) 패턴이 사라지고 데이터 클래스가 된다. 서브클래스가
  **동작**을 오버라이드하는 게 이 패턴의 요점. 억지 리팩터는 안 한다.

### Strategy 와의 차이 (실감한 점)

| | Template Method (이번) | Strategy (지난번) |
|--|--|--|
| 재사용 | 상속 — `Coffee(Beverage)` | 위임 — `Cart` 가 `DiscountPolicy` 를 필드로 보유 |
| 교체 시점 | 컴파일타임. 클래스 정의로 고정 | 런타임. `cart.set_discount(...)` |
| 바꾸는 범위 | 일부 단계 (`brew`, `add_condiments`) | 알고리즘 전체 (`apply`) |
| 흐름 제어 | 부모 `prepare()` 가 자식 단계 호출 | 클라이언트가 전략 주입, `Cart` 는 `apply` 만 호출 |

알고리즘 순서가 항상 같고 **일부 칸만** 바뀌면 Template Method.
알고리즘 자체를 통째로 갈아끼워야 하면 Strategy.

### 한계 / 주의

- **상속 강결합.** 서브클래스가 부모 구현에 묶인다. 부모의 단계 시그니처를 바꾸면
  모든 자식이 영향받는다. 조합 폭발(음료 × 우유종류 × 사이즈)이 생기면 상속으로는
  안 되고 Strategy/Decorator 조합이 낫다.
- **훅 남용 주의.** 훅이 많아지면 `prepare()` 가 `if` 범벅이 된다. 이때는 그 단계를
  통째로 Strategy 객체로 빼는 걸 고려.
