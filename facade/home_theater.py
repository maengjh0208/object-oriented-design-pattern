class Device:
    def __init__(self, log: list[str]):
        self.log = log


class DvdPlayer(Device):
    def on(self):
        self.log.append("dvd on")

    def off(self):
        self.log.append("dvd off")

    def play(self, movie: str):
        self.log.append(f"dvd play {movie}")

    def stop(self):
        self.log.append("dvd stop")

    def eject(self):
        self.log.append("dvd eject")


class Amplifier(Device):
    def on(self):
        self.log.append("amp on")

    def off(self):
        self.log.append("amp off")

    def set_dvd(self, dvd: DvdPlayer):
        self.log.append("amp set_dvd")

    def set_volume(self, level: int):
        self.log.append(f"amp volume {level}")


class Projector(Device):
    def on(self):
        self.log.append("projector on")

    def off(self):
        self.log.append("projector off")

    def wide_screen_mode(self):
        self.log.append("projector wide_screen")


class TheaterLights(Device):
    def on(self):
        self.log.append("lights on")

    def dim(self, level: int):
        self.log.append(f"lights dim {level}")


class Screen(Device):
    def up(self):
        self.log.append("screen up")

    def down(self):
        self.log.append("screen down")


class PopcornPopper(Device):
    def on(self):
        self.log.append("popper on")

    def off(self):
        self.log.append("popper off")

    def pop(self):
        self.log.append("popper pop")


class HomeTheaterFacade:
    def __init__(
        self,
        amp: Amplifier,
        dvd: DvdPlayer,
        projector: Projector,
        lights: TheaterLights,
        screen: Screen,
        popper: PopcornPopper,
    ):
        self.amp = amp
        self.dvd = dvd
        self.projector = projector
        self.lights = lights
        self.screen = screen
        self.popper = popper

    # Facade는 위임만 한다. 별도 로직 없다.
    # 서브시스템들은 Facade를 모른다.
    def watch_movie(self, movie: str):
        self.popper.on()
        self.popper.pop()
        self.lights.dim(10)
        self.screen.down()
        self.projector.on()
        self.projector.wide_screen_mode()
        self.amp.on()
        self.amp.set_dvd(self.dvd)
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)

    def end_movie(self):
        self.popper.off()
        self.lights.on()
        self.screen.up()
        self.projector.off()
        self.amp.off()
        self.dvd.stop()
        self.dvd.eject()
        self.dvd.off()
