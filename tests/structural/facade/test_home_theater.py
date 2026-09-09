from structural.facade.home_theater import (
    Amplifier,
    DvdPlayer,
    HomeTheaterFacade,
    PopcornPopper,
    Projector,
    Screen,
    TheaterLights,
)


def build_facade():
    log: list[str] = []
    amp = Amplifier(log)
    dvd = DvdPlayer(log)
    projector = Projector(log)
    lights = TheaterLights(log)
    screen = Screen(log)
    popper = PopcornPopper(log)
    facade = HomeTheaterFacade(amp, dvd, projector, lights, screen, popper)

    return facade, log


def test_watch_movie_runs_substems_in_order():
    facade, log = build_facade()

    facade.watch_movie("인터스텔라")

    assert log == [
        "popper on",
        "popper pop",
        "lights dim 10",
        "screen down",
        "projector on",
        "projector wide_screen",
        "amp on",
        "amp set_dvd",
        "amp volume 5",
        "dvd on",
        "dvd play 인터스텔라",
    ]


def test_end_movie_shuts_down_subsystems_in_order():
    facade, log = build_facade()

    facade.end_movie()

    assert log == [
        "popper off",
        "lights on",
        "screen up",
        "projector off",
        "amp off",
        "dvd stop",
        "dvd eject",
        "dvd off",
    ]


# Facade는 편의일 뿐 강제가 아님을 증명한다.
# 서브시스템은 Facade 없이 단독으로 사용할 수 있고, Facade를 import 및 참조하지 않는다.
def test_subsystem_works_without_facade():
    log: list[str] = []
    amp = Amplifier(log)

    amp.on()
    amp.set_volume(7)
    amp.off()

    assert log == ["amp on", "amp volume 7", "amp off"]


def test_client_can_reach_subsystem_directly_after_facade_macro():
    facade, log = build_facade()

    facade.watch_movie("인터스텔라")
    log.clear()

    facade.amp.set_volume(11)

    assert log == ["amp volume 11"]
