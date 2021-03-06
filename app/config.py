import logging
import os
from datetime import datetime, date

from dotenv import load_dotenv

from app.constants import ENV_DEV


class Config:
    load_dotenv()
    APP_NAME = 'ml-brand-gender-category'

    # Flask testing flag
    TESTING = False

    """
    If we do not set this all exceptions do not propagate to our error_handler
    Set DEBUG=false to test
    """
    PROPAGATE_EXCEPTIONS = True

    # Environment
    ENV = os.getenv('ENV', ENV_DEV)
    DEBUG = os.getenv('DEBUG', '1') == '1'

    # App configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5555))

    # Logging
    LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL', logging.DEBUG))

    # Pubsub config
    PUBSUB_HOST = os.getenv('PUBSUB_HOST')
    PUBSUB_PORT = os.getenv('PUBSUB_PORT')
    PUBSUB_PROTOCOL = os.getenv('PUBSUB_PROTOCOL')
    PUBSUB_PUBLISHER = 'ds-model'
    PUBSUB_EVENT_SENT = False
    PUBSUB_NAMESPACE = 'ml-brand-gender-category-api.recommendations'

    # Serialized model location
    MODEL_BASE_DIR = 'shared/ds-models'
    MODEL_BASE_DIR_S3 = 'ds-models'

    # Model id
    TRAINING_ID = os.getenv('TRAINING_ID')
    USE_CASE_ID = 'BRAND_GENDER_CATEGORY'
    MODEL_ID = 'CF'
    MODEL_VERSION_ID = '1.0'

    """
    REFERENCE DATA VALUES
    These vars are used to collect the reference point data. It's not run often, but refreshed
    every once in a while for sanity checks when training the models.
    """
    BGC_CUTPOINT = int(os.environ.get('REFERENCE_DATA_BGC_CUTPOINT', 0))
    CYCLE_COUNT = int(os.environ.get('REFERENCE_DATA_CYCLE_COUNT', 0))

    # ETL VALUES
    LAST_N_WEEKS = int(os.environ.get('ETL_LAST_N_WEEKS', 0))
    P_WEIGHT = int(os.environ.get('ETL_P_WEIGHT', 0))
    W_WEIGHT = int(os.environ.get('ETL_W_WEIGHT', 0))
    DECAY_WEIGHT = int(os.environ.get('ETL_DECAY_WEIGHT', 0))
    DECAY_WEIGHT_MULTIPLIER = float(os.environ.get('ETL_DECAY_WEIGHT_MULTIPLIER', 0.25))

    # DB VALUES
    SSENSE_DB_HOST = os.environ.get('SSENSE_DB_HOST')
    SSENSE_DB_USER = os.environ.get("SSENSE_DB_USER")
    SSENSE_DB_PWD = os.environ.get("SSENSE_DB_PWD")
    SSENSE_DB_DB = os.environ.get("SSENSE_DB_DB")
    STATS_DB_HOST = os.environ.get("STATS_DB_HOST")
    STATS_DB_USER = os.environ.get("STATS_DB_HOST")
    STATS_DB_PWD = os.environ.get("STATS_DB_PWD")
    STATS_DB_DB = os.environ.get("STATS_DB_DB")

    """AWS"""
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

    """SLACK"""
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

    """REDIS"""
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')


class ConfigTesting(Config):
    TESTING = True
    MODEL_BASE_DIR = 'tests/fixtures/loader_workspace'
    MODEL_FILE_NAME = 'model.pkl'
    DATAFRAME_FILE_NAME = 'data.pkl'
    USE_CASE_ID = 'brand-gender-category'
    MODEL_ID = 'm1'
    MODEL_VERSION_ID = 'v1'


class ConfigFunctionalTesting(ConfigTesting):
    pass


class ConfigUnitTesting(ConfigTesting):
    PUBSUB_HOST = 'a-test-pubsub-host'
    PUBSUB_PROTOCOL = 'https'
