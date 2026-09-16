from creational.singleton.app_config import AppConfig


def test_returns_same_instance():
    assert AppConfig() is AppConfig()


def test_has_default_settings():
    config = AppConfig()
    assert config.debug is False
    assert config.api_key is None


def test_mutated_state_survives_second_call():
    config = AppConfig()
    config.debug = True

    AppConfig()
    assert config.debug is True
