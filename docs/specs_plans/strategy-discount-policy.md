# Strategy — 할인 정책

- 분류: 행동 (Behavioral)
- 예제: 장바구니 할인 정책
- 구현 위치: `behavioral/strategy/`, 테스트 `tests/behavioral/strategy/`

---

## 1. 스펙

### 목표

장바구니 합계에 적용할 **할인 알고리즘을 교체 가능한 객체**로 분리한다.
새 할인 정책을 추가할 때 기존 코드(`Cart`)를 수정하지 않는다 (OCP).

### 등장 요소

| 역할 | 이름 | 책임 |
|------|------|------|
| Strategy | `DiscountPolicy` | `apply(price: int) -> int` 인터페이스 |
| ConcreteStrategy | `NoDiscount` | 할인 없음. 받은 값 그대로 반환 |
| ConcreteStrategy | `PercentageDiscount(rate)` | 정률 할인. `rate`는 0.0~1.0 |
| ConcreteStrategy | `FixedDiscount(amount)` | 정액 할인. 결과가 음수면 0 |
| Context | `Cart` | 상품 가격 목록 + 현재 할인 정책 보유. 합계에 정책 위임 |

### 동작 규칙

- 금액은 원 단위 `int`. 부동소수 오차를 피하려고 정수만 쓴다.
- `Cart.total()` = (상품 가격 합) 에 현재 정책 `apply()` 적용한 값.
- 상품이 없으면 합계 0, 정책 적용해도 0.
- `Cart.set_discount(policy)` 로 런타임에 정책을 바꾼다. 이후 `total()`은 새 정책을 반영.
- `PercentageDiscount`: 할인액 = `round(price * rate)`. `rate`가 0..1 밖이면 생성 시 `ValueError`.
- `FixedDiscount`: `max(0, price - amount)`. 음수 금액이 되지 않는다.
- 구조 제약: `NoDiscount` / `PercentageDiscount` / `FixedDiscount` 는 `Cart`를 import하지 않는다 (의존은 Context → Strategy 단방향).

### 왜 함수가 아니라 클래스인가

Python에서 전략은 그냥 함수여도 된다 (`Callable[[int], int]`).
여기서 클래스를 쓰는 이유: `PercentageDiscount`, `FixedDiscount`가 **설정값(rate, amount)을 상태로** 가진다.
상태 없는 순수 알고리즘이면 함수가 더 간단하다. 상태·검증이 붙으면 클래스가 값을 한다.

---

## 2. TDD 계획

red → green → refactor. 한 번에 테스트 하나.

| # | 실패 테스트 | 통과시키는 최소 구현 |
|---|-------------|----------------------|
| 1 | `NoDiscount().apply(10000) == 10000` | `DiscountPolicy` ABC + `NoDiscount` |
| 2 | 빈 `Cart().total() == 0` | `Cart.__init__`, `total()` 합산 |
| 3 | 상품 `[3000, 7000]` + `NoDiscount` → `total() == 10000` | `Cart`가 정책에 위임 |
| 4 | `PercentageDiscount(0.1)` 로 10000 → `total() == 9000` | `PercentageDiscount.apply` |
| 5 | `FixedDiscount(2000)` 로 10000 → `total() == 8000` | `FixedDiscount.apply` |
| 6 | `FixedDiscount(15000)` 로 10000 → `total() == 0` (음수 아님) | `max(0, ...)` |
| 7 | `cart.set_discount(PercentageDiscount(0.2))` 후 `total()` 변함 | `set_discount` |
| 8 | `PercentageDiscount(1.5)` → `ValueError` | 생성자 검증 |
| 9 | 구조: `behavioral.strategy` 하위 전략 모듈이 `cart`를 참조 안 함 | (검증만, 구현 불필요) |

리팩터 포인트: 3번 통과 후 `Cart.total()`의 합산/위임 분리, 중복 제거.

---

## 3. 결과 / 배운 점

### 최종 구조

```
behavioral/strategy/
  discount.py   # DiscountPolicy(ABC), NoDiscount, PercentageDiscount, FixedDiscount
  cart.py       # Cart (Context) — discount 참조 보유, total() 에서 위임
tests/behavioral/strategy/
  test_discount.py   # 전략 단위 테스트
  test_cart.py       # Context + 전략 조합 테스트
```

테스트 8개 통과.

### 배운 점

- **Context는 알고리즘을 모른다.** `Cart.total()` 은 `sum(items)` 만 하고 할인은
  `self._discount.apply(...)` 로 넘긴다. 할인 정책이 몇 개든 `Cart` 코드는 그대로.
  → 새 정책 추가 = `discount.py` 에 클래스 하나. OCP 충족.
- **`if/elif` 분기 vs 전략 객체**: 분기는 "행동 선택"을 호출 지점마다 반복하고,
  각 분기를 단독 테스트하기 어렵다. 전략은 각 알고리즘이 독립 클래스라 따로 테스트되고
  (`test_discount.py`), 런타임에 `set_discount()` 로 갈아끼운다.
- **널 오브젝트 (`NoDiscount`)**: "할인 없음"을 `None` 이 아니라 객체로 두면
  `Cart` 에 `if discount is None` 분기가 사라진다. 항상 `apply()` 호출 가능.
- **fail-fast 검증**: `PercentageDiscount` 의 `rate` 범위 체크를 `__init__` 에 둔다.
  잘못된 전략은 만들어지는 순간 막고, `apply()` 까지 미루지 않는다.
- **의존 방향**: 전략(`discount.py`)은 `cart` 를 import하지 않는다. `Cart → DiscountPolicy`
  단방향. Facade의 "서브시스템은 Facade를 모른다" 와 같은 원칙.
- **Python 대안**: 상태 없는 전략이면 클래스 대신 함수(`Callable[[int], int]`)로 충분.
  여기서는 `rate`/`amount` 라는 설정 상태와 검증이 있어서 클래스가 값을 한다.
  외부 임의 객체를 전략으로 받아야 하면 ABC 대신 `Protocol`.

### 혼동하기 쉬운 패턴과의 차이

- **State**: 구조가 거의 같다. 차이는 의도 — State는 내부 상태에 따라 객체가
  **스스로** 다음 상태로 전이한다. Strategy는 **클라이언트가** 전략을 골라 주입하고,
  전략끼리 서로를 모른다.
- **Template Method**: 알고리즘 골격을 상속으로 고정하고 일부 단계만 서브클래스가
  채운다 (컴파일 타임). Strategy는 알고리즘 전체를 위임으로 교체한다 (런타임).
