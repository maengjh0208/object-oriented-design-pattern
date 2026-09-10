# object-oriented-design-pattern

객체지향 디자인 패턴을 직접 구현하며 공부하는 레포. GoF의 23개 패턴을 생성/구조/행동
세 분류로 나누어 하나씩 다룬다. 각 패턴은 TDD로 구현하고, 스펙과 계획은
`docs/specs_plans/` 아래에 문서로 남긴다.

실행 방법과 프로젝트 규칙은 [`PROJECT.md`](PROJECT.md) 참고.

---

## 생성 패턴 (Creational)

객체를 어떻게 생성할지에 대한 패턴. 생성 로직을 캡슐화해 클라이언트가
구체 클래스에 직접 의존하지 않게 한다.

_아직 학습한 패턴 없음._

<!-- 예정: Singleton, Factory Method, Abstract Factory, Builder, Prototype -->

---

## 구조 패턴 (Structural)

클래스와 객체를 조합해 더 큰 구조를 만드는 패턴. 구성 요소 간의 관계를
정리해 유연하고 효율적인 구조를 얻는다.

### Facade

> 예제: 홈시어터 · 문서: [`docs/specs_plans/facade-home-theater.md`](docs/specs_plans/facade-home-theater.md)

**무엇인가**
복잡한 서브시스템 여러 개(앰프, DVD 플레이어, 프로젝터, 조명, 스크린, 팝콘 기계)를
단순한 진입점 하나로 감싸는 패턴. 클라이언트는 서브시스템 내부를 몰라도 된다.

**왜 사용하는가**
- 클라이언트가 서브시스템 클래스 여러 개를 직접 알고, 호출 순서와 의존성까지
  챙겨야 하면 결합도가 높아진다. 서브시스템이 바뀌면 클라이언트가 전부 깨진다.
- Facade가 그 조합·순서 로직을 흡수하면, 클라이언트 코드는 `facade.watch_movie("영화")`
  한 줄로 끝난다.
- 서브시스템과 클라이언트 계층을 느슨하게 연결한다.

**어떻게 구현하는가**
1. Facade 클래스가 서브시스템 객체들을 참조로 보유한다.
2. 클라이언트가 원하는 고수준 동작(`watch_movie`, `end_movie`)을 메서드로 노출하고,
   그 안에서 서브시스템 메서드를 정해진 순서로 위임 호출한다.
3. Facade에는 비즈니스 로직을 넣지 않는다. 조합과 위임만 한다.
   (로직이 쌓이면 God object가 된다.)
4. 서브시스템은 Facade의 존재를 모른다. 단독으로도 사용 가능해야 한다 (단방향 의존).
5. Facade는 서브시스템 직접 접근을 막지 않는다. 편의를 제공할 뿐 강제가 아니다.

```python
class HomeTheaterFacade:
    def __init__(self, amp, dvd, projector, lights, screen, popper):
        self.amp, self.dvd, self.projector = amp, dvd, projector
        self.lights, self.screen, self.popper = lights, screen, popper

    def watch_movie(self, movie):
        self.popper.on(); self.popper.pop()
        self.lights.dim(10)
        self.screen.down()
        self.projector.on(); self.projector.wide_screen_mode()
        self.amp.on(); self.amp.set_dvd(self.dvd); self.amp.set_volume(5)
        self.dvd.on(); self.dvd.play(movie)
```

**혼동하기 쉬운 패턴과의 차이**
- **Adapter**: 인터페이스를 *변환*한다(호환성). Facade는 인터페이스를 *단순화*한다(여러 개 → 하나).
- **Mediator**: 동료 객체 사이를 *양방향*으로 조정한다. Facade는 *단방향* 단순화만 한다.

**주의점**
- 서브시스템 간 결합(`Amplifier`가 `DvdPlayer`를 입력 소스로 아는 것)은 도메인
  고유의 것이다. Facade가 없애는 건 이게 아니라, 클라이언트가 그 배선을 직접 하는 상황이다.

<!-- 예정: Adapter, Bridge, Composite, Decorator, Flyweight, Proxy -->

---

## 행동 패턴 (Behavioral)

객체 사이의 책임 분배와 상호작용, 알고리즘에 대한 패턴.

### Strategy

> 예제: 장바구니 할인 정책 · 문서: [`docs/specs_plans/strategy-discount-policy.md`](docs/specs_plans/strategy-discount-policy.md)

**무엇인가**
알고리즘군(정률 할인, 정액 할인, 할인 없음)을 각각 객체로 캡슐화해서
교체 가능하게 만드는 패턴. 알고리즘을 쓰는 쪽(`Cart`)과 알고리즘 자체(`DiscountPolicy`)를 분리한다.

**왜 사용하는가**
- 행동을 `if method == "percent": ... elif ...` 로 고르면, 정책 추가 때마다 그 분기를
  수정해야 하고(OCP 위반), 각 알고리즘을 단독으로 테스트하기 어렵다.
- 각 알고리즘을 `DiscountPolicy` 구현 클래스로 빼면, `Cart` 는 인터페이스에만 의존한다.
  새 정책은 클래스 하나 추가로 끝나고, `cart.set_discount(...)` 로 런타임에 갈아끼운다.

**어떻게 구현하는가**
1. `DiscountPolicy` (ABC): `apply(price: int) -> int` 하나만 가진 인터페이스.
2. 구현체들: `NoDiscount`(그대로 반환 — 널 오브젝트), `PercentageDiscount(rate)`,
   `FixedDiscount(amount)`.
3. `Cart` (Context): `DiscountPolicy` 참조를 보유하고 `total()` 에서 위임한다.
   할인 계산 로직은 `Cart` 에 없다.
4. 잘못된 설정값은 전략 생성자에서 막는다 (`PercentageDiscount` 의 `rate` 범위 검증).

```python
class DiscountPolicy(ABC):
    @abstractmethod
    def apply(self, price: int) -> int: ...

class PercentageDiscount(DiscountPolicy):
    def __init__(self, rate: float):
        if not 0 <= rate <= 1:
            raise ValueError("Rate must be between 0 and 1")
        self._rate = rate
    def apply(self, price: int) -> int:
        return price - round(price * self._rate)

class Cart:
    def __init__(self, discount: DiscountPolicy | None = None):
        self._items: list[int] = []
        self._discount = discount or NoDiscount()
    def total(self) -> int:
        return self._discount.apply(sum(self._items))
```

**혼동하기 쉬운 패턴과의 차이**
- **State**: 구조는 거의 같다. State는 객체가 내부 상태에 따라 *스스로* 전이한다.
  Strategy는 *클라이언트가* 전략을 골라 주입하고, 전략끼리 서로를 모른다.
- **Template Method**: 알고리즘 골격을 상속으로 고정하고 일부 단계만 오버라이드(컴파일 타임).
  Strategy는 알고리즘 전체를 위임으로 교체(런타임).

**주의점**
- 상태 없는 알고리즘이면 Python에선 클래스 대신 함수로도 충분하다. 설정값·검증이
  붙을 때 클래스가 값을 한다.

### Template Method

> 예제: 음료 제조 (커피/홍차) · 문서: [`docs/specs_plans/template-method-beverage.md`](docs/specs_plans/template-method-beverage.md)

**무엇인가**
알고리즘의 골격(물 끓이기 → 우리기 → 따르기 → 첨가물)을 부모 클래스의 메서드
하나에 고정하고, 달라지는 단계(우리는 법, 첨가물)만 서브클래스가 채우는 패턴.
공통 흐름은 부모에 한 번만 존재한다.

**왜 사용하는가**
- 여러 클래스가 큰 흐름은 똑같고 몇 단계만 다르면, 그 흐름을 각 클래스에 복사하게 된다.
  한 곳을 고치면 나머지를 다 따라 고쳐야 한다.
- 흐름을 부모 `prepare()` 에 두고 변하는 단계만 추상 메서드로 열어두면, 서브클래스
  코드는 "변하는 부분만" 남는다. 흐름 수정은 부모 한 곳.
- **할리우드 원칙**: 자식이 부모를 부르지 않는다. 부모 `prepare()` 가 자식이 채운
  `brew()` 를 부른다. 흐름 제어권이 부모에 있다.

**어떻게 구현하는가**
1. `Beverage` (ABC): `prepare()` 템플릿 메서드가 단계 호출 순서를 고정한다.
   이 메서드는 오버라이드하지 않는다.
2. 공통 단계(`boil_water`, `pour_in_cup`)는 부모가 구현한다.
3. 변하는 단계(`brew`, `add_condiments`)는 `@abstractmethod` — 자식이 반드시 구현.
4. 훅(`wants_condiments`)은 기본 구현이 있는 메서드. 자식이 원할 때만 오버라이드해
   흐름에 개입한다. `BlackCoffee` 는 이 훅만 `False` 로 바꿔 첨가물 단계를 건너뛴다.

```python
class Beverage(ABC):
    def __init__(self) -> None:
        self.steps: list[str] = []

    def prepare(self) -> None:          # 템플릿 메서드 — 순서 고정
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.wants_condiments():     # 훅으로 분기
            self.add_condiments()

    def boil_water(self) -> None: self.steps.append("물 끓이기")
    def pour_in_cup(self) -> None: self.steps.append("컵에 따르기")

    @abstractmethod
    def brew(self) -> None: ...
    @abstractmethod
    def add_condiments(self) -> None: ...

    def wants_condiments(self) -> bool: return True   # 훅

class Coffee(Beverage):
    def brew(self) -> None: self.steps.append("커피 필터로 내리기")
    def add_condiments(self) -> None: self.steps.append("설탕과 우유 추가")

class BlackCoffee(Coffee):
    def wants_condiments(self) -> bool: return False
```

**혼동하기 쉬운 패턴과의 차이**
- **Strategy**: 알고리즘 전체를 위임으로 교체(런타임, has-a). Template Method는
  골격을 상속으로 고정하고 일부 단계만 오버라이드(컴파일 타임, is-a).
- **Factory Method**: Template Method의 특수한 경우 — 자식이 채우는 단계가
  "객체 생성" 인 것.

**주의점**
- 상속 강결합. 부모 단계 시그니처를 바꾸면 모든 자식이 영향받는다. 조합이 폭발하면
  (음료 × 우유 × 사이즈) 상속으로 안 되고 Strategy/Decorator 조합이 낫다.
- 훅이 많아지면 `prepare()` 가 `if` 범벅이 된다. 그 단계를 Strategy 객체로 빼는 걸 고려.

<!-- 예정: Observer, Command, State, Iterator,
     Chain of Responsibility, Mediator, Memento, Visitor, Interpreter -->
