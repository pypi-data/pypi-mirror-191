"""Testing configuration settings."""
from monopyly.config.default_settings import Config


class TestingConfig(Config):
    """A configuration object with settings for testing."""
    TESTING = True

