from typing import Tuple, Type, Dict, NoReturn

from flask_injector import FlaskInjector
import injector
from flask import Flask
from flask_restful import Api
from ssense_logger.app_logger import AppLogger

from app.config import Config
from app.entities.model.model_info import ModelInfo
from app.library.model_repository.loader.driver.filesystem import Filesystem
from app.library.model_repository.repository import Repository
from app.server.middlewares.error_middleware import add_error_handler
from app.server.services.predict import PredictService
from .middlewares.record_access_log import record_access_log
from .middlewares.record_request_id import record_request_id
from .middlewares.record_time_of_request import record_time_of_request
from app.server.providers import AppLoggerModule
from .resources.health import Health
from .resources.predict import Predict
from .resources.home import Home
from .resources.readiness import Readiness
from .resources.liveness import Liveness
from app.repositories.redis_repository import RedisRepository


def create_app(config: Type[Config] = Config) -> Tuple[Flask, Api]:
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(config)

    """----------------- Logging -----------------"""
    app_logger = AppLogger(app_name=config.APP_NAME, env=config.ENV)

    """----------------- Middleware ---------------------"""
    # Before Request
    # Perform these functions in the declared order before every request.
    app.before_request_funcs = {None: [record_time_of_request,
                                       record_request_id]}

    # After Request
    # Perform this function after every request.
    app.after_request(record_access_log)

    """----------------- Bind Resources -----------------"""
    api.add_resource(Health, '/healthcheck')
    api.add_resource(Liveness, '/liveness')
    api.add_resource(Readiness, '/readiness', resource_class_kwargs={'config': app.config, 'app_logger': app_logger})

    # Initialize redis repository
    redis_repository = RedisRepository(
        config,
        app_logger
    )

    loader = Filesystem(Repository(config.MODEL_BASE_DIR))

    model_info = ModelInfo(
        config.USE_CASE_ID,
        config.MODEL_ID,
        config.MODEL_VERSION_ID,
        config.TRAINING_ID
    )

    app_logger.info(msg="Loading model from file..")
    model = loader.load_model(model_info)

    api.add_resource(Predict, '/predict', resource_class_kwargs={
        'predict_service': PredictService(
            model=model,
            app_logger=app_logger,
            customer_bgc_scores_repository=redis_repository),
        'app_logger': app_logger
    })
    api.add_resource(Home, '/', resource_class_kwargs={
        'config': app.config,
        'model_info': model.to_model_info(),
        'app_logger': app_logger
    })

    add_error_handler(app)

    return app, api


def _configure_dependency_injection(flask_app: Flask,
                                    custom_injector: injector.Injector = None,
                                    extra_injector_modules: Dict = None) -> NoReturn:
    modules = {
        'app_logger': AppLoggerModule(flask_app.config['APP_NAME'], flask_app.config['ENV']).create()
    }
    if extra_injector_modules:
        modules.update(extra_injector_modules)

    FlaskInjector(
        app=flask_app,
        injector=custom_injector,
        modules=modules.values(),
    )
