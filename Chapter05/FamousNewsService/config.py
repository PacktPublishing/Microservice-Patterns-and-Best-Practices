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
        'db': 'famous_dev',
        'host': '{}{}'.format(
            os.environ.get('DATABASE_HOST'),
            'famous_dev',
        ),
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'famous_test',
        'host': '{}{}'.format(
            os.environ.get('DATABASE_HOST'),
            'famous_test',
        ),
    }


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': 'famous',
        'host': '{}{}'.format(
            os.environ.get('DATABASE_HOST'),
            'famous',
        ),
    }
