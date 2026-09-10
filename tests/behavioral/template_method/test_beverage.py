import pytest

from behavioral.template_method.beverage import Beverage, BlackCoffee, Coffee, Tea


def test_coffee_prepare_follows_fixed_step_order():
    coffee = Coffee()

    coffee.prepare()

    assert coffee.steps == [
        "물 끓이기",
        "커피 필터로 내리기",
        "컵에 따르기",
        "설탕과 우유 추가",
    ]


def test_tea_prepare_follows_fixed_step_order():
    tea = Tea()

    tea.prepare()

    assert tea.steps == [
        "물 끓이기",
        "티백 우려내기",
        "컵에 따르기",
        "레몬 추가",
    ]


def test_beverage_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Beverage()


def test_black_coffee_skips_condiments_via_hook():
    black = BlackCoffee()

    black.prepare()

    assert black.steps == [
        "물 끓이기",
        "커피 필터로 내리기",
        "컵에 따르기",
    ]


def test_subclasses_do_not_redefine_the_common_flow():
    # cls.__dict__ 은 그 클래스에 직접 정의된 것만 담는다. (상속받은 건 안들어감)
    # 공통 흐름은 부모 클래스만 소유하는지 확인. 자식 클래스에서 오버라이드 하면 안됨 (패턴 위반)
    for cls in (Coffee, Tea):
        assert "prepare" not in cls.__dict__
        assert "boil_water" not in cls.__dict__
        assert "pour_in_cup" not in cls.__dict__
