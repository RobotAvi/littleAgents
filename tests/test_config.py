from shared.config import Config

def test_get_utility_config():
    config = Config.get_utility_config("test")
    assert isinstance(config, dict)