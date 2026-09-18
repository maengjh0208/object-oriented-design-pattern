# Adapter — 결제 게이트웨이

- 분류: 구조 (Structural)
- 예제: 결제 게이트웨이 어댑터 (서드파티 `LegacyGateway`를 우리 시스템 인터페이스로 감싸기)
- 구현 위치: `structural/adapter/`, 테스트 `tests/structural/adapter/`

---

## 1. 스펙

### 목표

우리 시스템은 `PaymentProcessor.pay(amount: float) -> bool` 인터페이스를 기대하는데,
실제 붙여야 할 서드파티 결제 라이브러리(`LegacyGateway`)는 전혀 다른 시그니처
(`make_payment(amount_in_cents: int, currency: str) -> dict`)를 가진다. `LegacyGateway`는
코드 수정이 불가하다고 가정하고, 그 간극을 Adapter로 메꾼다.

### 등장 요소

| 역할 | 이름 | 책임 |
|------|------|------|
| Target (추상) | `PaymentProcessor` | 우리 시스템이 기대하는 인터페이스: `pay(amount: float) -> bool` |
| Adaptee | `LegacyGateway` | 서드파티 결제 라이브러리. `make_payment(amount_in_cents, currency) -> dict`, 코드 수정 불가 |
| Adapter | `PaymentGatewayAdapter` | `PaymentProcessor` 구현. `LegacyGateway` 인스턴스를 합성으로 보유하고 위임 |

### 동작 규칙

- `LegacyGateway.make_payment`는 **센트 단위 정수**를 받는다. 금액이 0 이하면
  `{"success": False, ...}`, 아니면 `{"success": True, ...}`.
- `PaymentGatewayAdapter.pay(amount)`는 `amount`(원 단위 `float`)를
  `round(amount * 100)`으로 센트 변환 후 `LegacyGateway.make_payment`를 호출하고,
  `result["success"]`만 뽑아 `bool`로 반환한다.
- 통화는 `"USD"` 고정 (멀티 통화는 범위 밖 — YAGNI).

---

## 2. TDD 계획

red → green. 한 번에 테스트 하나.

| # | 실패 테스트 | 통과시키는 최소 구현 |
|---|-------------|----------------------|
| 1 | 스파이(`SpyLegacyGateway`)로 `pay(10.0)` 호출 시 `make_payment(1000, "USD")`로 불렸는지 확인 | `PaymentProcessor`(Target) + `PaymentGatewayAdapter`(단위 변환 + 위임) |
| 2 | 진짜 `LegacyGateway`로 `pay(10.0)` → `True` | `LegacyGateway` 실제 구현 |
| 3 | `pay(0)` → `False` | (구현 추가 없음 — `LegacyGateway`의 검증이 위임을 통해 그대로 전달됨을 확인) |

---

## 3. 결과 / 배운 점

### 최종 구조

```
structural/adapter/
  payment_processor.py         # Target — PaymentProcessor(ABC), pay(amount) -> bool
  legacy_gateway.py             # Adaptee — LegacyGateway, make_payment(cents, currency) -> dict
  payment_gateway_adapter.py    # Adapter — PaymentGatewayAdapter(PaymentProcessor), 합성 + 단위 변환
tests/structural/adapter/
  test_payment_gateway_adapter.py   # 변환 검증(스파이) + 정상/비정상 금액(실제 Adaptee)
```

```python
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool: ...


class LegacyGateway:
    def make_payment(self, amount_in_cents: int, currency: str) -> dict:
        if amount_in_cents <= 0:
            return {"success": False, "error": "invalid amount"}
        return {"success": True, "charged_cents": amount_in_cents, "currency": currency}


class PaymentGatewayAdapter(PaymentProcessor):
    def __init__(self, legacy_gateway):
        self._legacy_gateway = legacy_gateway

    def pay(self, amount: float) -> bool:
        cents = round(amount * 100)
        result = self._legacy_gateway.make_payment(cents, "USD")
        return result["success"]
```

테스트 3개 통과, ruff clean.

### 배운 점

- **Adapter는 기존 걸 안 고친다.** `LegacyGateway`는 한 줄도 안 바뀐다. Adapter는 밖에서
  감싸서 다른 모양으로 보이게 할 뿐, 안을 뜯어고치는 게 아니다. "레거시 현대화"라기보다
  **"바꿀 수 없는 인터페이스를 겉에서 감싸 호환되게 만드는 것"**이 정확한 정의.
- **핵심은 레거시가 아니라 "인터페이스 불일치 + 못/안 바꾸는 대상"이다.** 레거시 코드가
  제일 흔한 이유일 뿐, 최신 서드파티 라이브러리도, 심지어 우리 팀이 만든 두 모듈이라도
  컨벤션이 다르면 Adapter로 이어붙일 수 있다.
- **변환 자체를 검증하려면 결과값만 봐선 부족하다.** `pay()`의 반환값(`bool`)만 확인하면
  "단위를 실제로 원→센트로 변환해서 불렀는지"는 증명이 안 된다. 호출 인자를 기록하는
  스파이(spy, 테스트 더블의 일종)를 써서 `make_payment(1000, "USD")`로 정확히 불렸는지
  직접 확인했다. 결과 검증과 "어떻게 호출했는지" 검증은 다른 질문이다.
- **Target 인터페이스는 여러 Adaptee가 있어야 값을 발휘한다.** Adaptee가 `LegacyGateway`
  하나뿐인 지금 상태에서는, `PaymentProcessor` ABC 없이 그냥 평범한 wrapper 클래스로
  짜도 기능적으로 동일하다. 다형성(여러 게이트웨이를 갈아끼워도 클라이언트 코드가
  안 바뀌는 것)이 Adapter의 핵심 가치인데, 이번 예제 범위(Adaptee 1개)에서는
  **그 가치가 실제로 발휘되지 않았다.** 격리(우리 코드가 `LegacyGateway`의 구체적인
  모양에 안 묶이는 것)라는 부차적 이점만 확인했다.

### Facade와의 차이 (다시 정리)

| | Adapter (이번) | Facade |
|--|--|--|
| 목적 | 인터페이스 **변환** (호환성) | 여러 인터페이스 **단순화** (진입점 하나) |
| 감싸는 대상 | 보통 하나(호환 안 되는 기존 클래스) | 여러 개(서브시스템들) |
| 로직 | 형식 변환만, 새 로직 없음 | 조합·순서 로직 있음 |

### 한계 / 주의

- **다형성 이점을 이번 예제에서 실제로 보여주지 못했다.** Adaptee가 하나뿐이라
  `PaymentProcessor` ABC가 지금은 장식에 가깝다. 두 번째 게이트웨이(다른 시그니처)가
  추가되고, 그걸 받는 클라이언트 함수(`checkout(processor: PaymentProcessor, ...)`)가
  생겨야 진가가 보인다. 억지로 두 번째 예제를 붙이는 대신, 이 한계를 있는 그대로
  기록하는 쪽을 택했다.
- **부동소수점으로 금액 계산.** `round(amount * 100)`은 `float`의 부동소수점 오차에
  취약하다(`0.1 + 0.2 != 0.3` 같은 문제가 금액 계산에서도 생길 수 있음). 실무에선
  `Decimal`이나 정수 최소단위 관리가 정석. 이 예제는 Adapter 패턴 자체가 목적이라
  고치지 않고 한계로만 남긴다.
- **Adaptee가 예외를 던지는 경우 처리 안 함.** `LegacyGateway.make_payment`가 항상
  예외 없이 `dict`를 반환한다고 전제한다. 실제 서드파티 라이브러리가 네트워크 에러
  등으로 예외를 던지면 `PaymentGatewayAdapter`가 그대로 전파한다 — 감싸서 변환해주지
  않는다. 이번 예제 시나리오 밖이라 다루지 않음.
