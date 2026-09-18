# State — 주문 상태

- 분류: 행동 (Behavioral)
- 예제: 주문 상태 (결제대기 → 결제완료 → 배송중 → 배송완료, 취소)
- 구현 위치: `behavioral/state/`, 테스트 `tests/behavioral/state/`

---

## 1. 스펙

### 목표

주문의 동작(결제, 배송 시작, 배송완료, 취소)이 현재 상태에 따라 다르게 반응하도록 만든다.
상태마다 허용되는 전이가 다르다 — 예를 들어 배송중 이후엔 취소할 수 없다.
`if/elif`로 상태를 분기하는 대신, 상태 하나하나를 클래스로 캡슐화한다.

### 등장 요소

| 역할 | 이름 | 책임 |
|------|------|------|
| State (추상) | `OrderStatus` | 공통 인터페이스: `pay`, `ship`, `deliver`, `cancel`. 기본 구현은 전부 `InvalidTransitionError` |
| ConcreteState | `Pending` (결제대기) | `pay` → `Paid`로 전이, `cancel` → `Cancelled`로 전이 |
| ConcreteState | `Paid` (결제완료) | `ship` → `Shipping`로 전이, `cancel` → `Cancelled`로 전이 |
| ConcreteState | `Shipping` (배송중) | `deliver` → `Delivered`로 전이 (취소 불가, 기본 에러 그대로) |
| ConcreteState | `Delivered` (배송완료) | 종단 상태, 오버라이드 없음(모든 동작 에러) |
| ConcreteState | `Cancelled` (취소됨) | 종단 상태, 오버라이드 없음(모든 동작 에러) |
| Context | `Order` | 현재 상태 객체(`_status`)를 보유, 호출을 위임. `status` 프로퍼티로 현재 상태 이름 노출 |
| 예외 | `InvalidTransitionError` | 현재 상태에서 허용 안 되는 전이 시도 시 발생 |

### 동작 규칙

- `OrderStatus`의 `pay`/`ship`/`deliver`/`cancel` 기본 구현은 전부 `InvalidTransitionError`를 던진다.
  각 상태는 **자기가 허용하는 전이만** 오버라이드한다.
- 전이는 상태 객체 자신이 결정한다: `order.status = NextState()` (프로퍼티 세터로 상태 객체 교체).
- `Order`는 생성 시 `Pending()`으로 시작.
- 상태 이름 확인은 `order.status`(getter) → `type(self._status).__name__` 반환.

---

## 2. TDD 계획

red → green. 한 번에 테스트 하나.

| # | 실패 테스트 | 통과시키는 최소 구현 |
|---|-------------|----------------------|
| 1 | `Order()` → `status == "Pending"` | `Order.__init__`에서 `Pending()` 세팅, `status` 프로퍼티 |
| 2 | `pay()` → `status == "Paid"` | `Pending.pay` 구현 + `Order.pay` 위임 |
| 3 | `pay(); ship()` → `status == "Shipping"` | `Paid.ship` 구현 + `Order.ship` 위임 |
| 4 | `pay(); ship(); deliver()` → `status == "Delivered"` | `Shipping.deliver` 구현 + `Order.deliver` 위임 |
| 5 | `cancel()` (결제대기) → `status == "Cancelled"` | `Pending.cancel` 구현 + `Order.cancel` 위임 |
| 6 | `pay(); cancel()` → `status == "Cancelled"` | `Paid.cancel` 구현 |
| 7 | `pay(); ship(); cancel()` → `InvalidTransitionError` | `OrderStatus` 기본 메서드를 `pass`에서 `raise`로 전환 |

---

## 3. 결과 / 배운 점

### 최종 구조

```
behavioral/state/
  order.py          # Order (Context) — _status 위임, status 프로퍼티(getter: 이름 문자열, setter: 상태 객체 교체)
  order_status.py    # OrderStatus(기본, 전부 raise) + Pending/Paid/Shipping/Delivered/Cancelled
                      # InvalidTransitionError
tests/behavioral/state/
  test_order.py       # 정상 전이 5개 + 잘못된 전이 1개(에러) + 초기 상태 1개
```

```python
class OrderStatus:
    def pay(self, order):
        raise InvalidTransitionError(f"{type(self).__name__} 상태에서는 결제할 수 없습니다")

    # ship, deliver, cancel 동일 패턴


class Pending(OrderStatus):
    def pay(self, order):
        order.status = Paid()

    def cancel(self, order):
        order.status = Cancelled()


class Order:
    def __init__(self):
        self._status = Pending()

    @property
    def status(self):
        return type(self._status).__name__

    @status.setter
    def status(self, state):
        self._status = state

    def pay(self):
        self._status.pay(self)
```

테스트 7개 통과, ruff clean.

### 배운 점

- **기본 구현이 "에러"인 훅.** Template Method의 훅은 기본값이 안전한 no-op(`return True`)이었는데,
  State는 반대로 기본값이 `raise`다. "허용 안 된 전이는 막아야 한다"가 기본이고, 각 상태는
  자기가 허용하는 예외 케이스만 오버라이드한다. 같은 "기본 구현 + 선택적 오버라이드" 틀인데
  기본값의 방향이 문제 성격에 따라 다르다.
- **상태 전이는 상태 객체 자신이 안다.** `Order`는 "지금 상태가 뭔지, 다음에 뭐가 되는지" 전혀
  모른다. `Pending.pay`가 `order.status = Paid()`로 직접 다음 상태를 만들어 꽂는다. `Order`는
  위임만 할 뿐 전이 로직이 전혀 없다.
- **순환 참조를 실제로 겪었다.** `OrderStatus.pay(self, order: Order)`처럼 타입 힌트를 정확히
  적으려다 `order_status.py`가 `order.py`를 import하고, `order.py`도 `order_status.py`를
  import하는 양방향 참조가 생겨 `ImportError`가 났다. 해법으로 `TYPE_CHECKING` 가드를 검토했지만,
  이 프로젝트엔 애초에 정적 타입 검사기(mypy 등)가 없어서 타입 힌트가 순수 문서 목적일 뿐임을
  확인하고, 그냥 duck typing으로 힌트를 뺐다. **정적 검사기 없는 프로젝트에서 타입 힌트 때문에
  순환 참조를 만드는 건 얻는 것보다 잃는 게 크다.**
- **TDD가 진짜로 오타를 잡아줬다.** `Order.deliver()`를 `self._status.deliver(self)` 위임 없이
  `pass`로 잘못 짰을 때, 테스트가 `'Shipping' == 'Delivered'`로 정확히 실패 지점을 짚어줬다.
  반대로 `assert`를 빼먹은 테스트는 아무것도 안 잡아준다 — 테스트 자체가 검증문 없으면
  통과해도 의미 없다는 것도 실감했다.
- **`status` 프로퍼티의 getter/setter가 비대칭이다.** getter는 상태 이름(문자열, `"Paid"`)을
  반환하는데 setter는 상태 객체(`Paid()` 인스턴스)를 받는다. `order.status = order.status`가
  성립 안 하는 비대칭 프로퍼티 — 읽기 쉬우라고 문자열로 노출한 대가. 헷갈리면
  `set_state(state)`처럼 별도 메서드로 분리하는 게 더 명확할 수 있다.

### Strategy / Template Method 와의 차이 (실감한 점)

| | State (이번) | Strategy | Template Method |
|--|--|--|--|
| 재사용 | 위임 — `Order`가 `OrderStatus` 필드 보유 | 위임 — `Cart`가 `DiscountPolicy` 필드 보유 | 상속 — `Coffee(Beverage)` |
| 전이/교체 주체 | **상태 객체 자신**이 다음 상태로 전이 | **클라이언트**가 전략을 골라 주입 | 컴파일타임, 클래스 정의로 고정 |
| 서로를 아는가 | 상태들이 서로 다음 상태 클래스를 앎 | 전략끼리 서로 모름 | 자식이 부모 골격만 앎 |
| 목적 | 상태에 따라 동작이 달라짐을 표현 | 알고리즘 전체를 교체 가능하게 | 알고리즘 골격 고정, 일부 단계만 교체 |

구조(Context가 교체 가능한 객체를 필드로 들고 위임)는 Strategy와 똑같이 생겼는데,
"누가 전이를 결정하는가"가 근본적으로 다르다 — State는 객체가 스스로, Strategy는 바깥에서.

### 한계 / 주의

- **상태 클래스가 상태를 안 갖는다(무상태).** `Pending`, `Paid` 등은 인스턴스 필드가 없어서
  사실 싱글턴처럼 재사용해도 되는데, 지금은 전이할 때마다 `Paid()`처럼 매번 새로 만든다.
  상태 개수가 적어 문제는 안 되지만, 상태가 많아지고 자주 전이하면 상태 객체를 캐싱하는
  최적화도 고려할 수 있다(과한 최적화라 지금은 안 함).
- **상태 폭발.** 상태 × 이벤트 조합이 늘어나면(`OrderStatus`에 메서드가 계속 추가되면)
  클래스마다 오버라이드할 게 늘어난다. 상태 전이표가 복잡해지면 상태 다이어그램을
  먼저 그려보고 시작하는 게 낫다.
