"""Development configuration settings."""
from monopyly.config.default_settings import Config


class DevelopmentConfig(Config):
    """A configuration object with settings for development."""
    DEBUG = True
    SECRET_KEY = "development key"

