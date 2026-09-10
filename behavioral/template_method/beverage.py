from abc import ABC, abstractmethod


class Beverage(ABC):
    def __init__(self) -> None:
        self.steps: list[str] = []

    def prepare(self) -> None:
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.wants_condiments():
            self.add_condiments()

    def boil_water(self) -> None:
        self.steps.append("물 끓이기")

    def pour_in_cup(self) -> None:
        self.steps.append("컵에 따르기")

    @abstractmethod
    def brew(self) -> None:
        pass

    @abstractmethod
    def add_condiments(self) -> None:
        pass

    def wants_condiments(self) -> bool:
        return True


class Coffee(Beverage):
    def brew(self) -> None:
        self.steps.append("커피 필터로 내리기")

    def add_condiments(self) -> None:
        self.steps.append("설탕과 우유 추가")


class BlackCoffee(Coffee):
    def wants_condiments(self) -> bool:
        return False


class Tea(Beverage):
    def brew(self) -> None:
        self.steps.append("티백 우려내기")

    def add_condiments(self) -> None:
        self.steps.append("레몬 추가")
