"""Development configuration settings."""
from monopyly.config.default_settings import Config


class ProductionConfig(Config):
    """A configuration object with settings for production."""
    SECRET_KEY = "INSECURE PRODUCTION TEST KEY"

