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

_아직 학습한 패턴 없음._

<!-- 예정: Strategy, Observer, Command, State, Template Method, Iterator,
     Chain of Responsibility, Mediator, Memento, Visitor, Interpreter -->
