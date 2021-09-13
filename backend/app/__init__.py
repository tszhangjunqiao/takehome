from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from celery import Celery
# from flask_celery import Celery

from config import CONFIG

from utils.ocr import OCRer
# from app.extensions import config_extensions

# 创建数据库
db = SQLAlchemy()
ocrer = OCRer(CONFIG.OCR_LANGUAGE, CONFIG.OCR_GPU)
migrate = Migrate()

def create_app():

    # 初始化
    app = Flask(__name__)

    # 导致指定的配置对象:创建app时，传入环境的名称
    app.config.from_object(CONFIG)

    # 初始化扩展（数据库）
    db.init_app(app)

    migrate.init_app(app, db)

    # config_extensions(app)

    # 创建数据库表
    create_tables(app)

    # 注册所有蓝本
    regist_blueprints(app)

    return app


def regist_blueprints(app):
    from app.api import api

    # 注册api蓝本,url_prefix为所有路由默认加上的前缀
    app.register_blueprint(api, url_prefix='/api')


def create_tables(app):
    from app.models import FileUpload, Tasks, Results
    db.create_all(app=app)


def make_celery(app):
    """Create the celery process."""

    # Init the celery object via app's configuration.
    celery = Celery(
        app.import_name,
        backend=CONFIG.CELERY_RESULT_BACKEND,
        broker=CONFIG.CELERY_BROKER_URL)

    # Flask-Celery-Helpwe to auto-setup the config.
    # celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            """Will be execute when create the instance object of ContextTesk."""

            # Will context(Flask's Extends) of app object(Producer Sit)
            # be included in celery object(Consumer Site).
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    # Include the app_context into celery.Task.
    # Let other Flask extensions can be normal calls.
    celery.Task = ContextTask
    return celery
