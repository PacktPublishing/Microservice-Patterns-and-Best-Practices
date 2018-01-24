import os

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {}


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'sports_dev',
        'host': '{}{}'.format(
            os.environ.get('DATABASE_HOST'),
            'sports_dev',
        ),
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'sports_test',
        'host': '{}{}'.format(
            os.environ.get('DATABASE_HOST'),
            'sports_test',
        ),
    }


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': 'sports',
        'host': '{}{}'.format(
            os.environ.get('DATABASE_HOST'),
            'sports',
        ),
    }
