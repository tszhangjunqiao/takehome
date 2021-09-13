#!/usr/bin/env python

import sys
import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfigs(object):
    def __getitem__(self, item):
        return self.__getattribute__(item)

    PORT = 8888

    WORK_PATH = os.getcwd()
    LOG_PATH = os.path.join(os.getcwd(), "all.log")
    UPLOAD_PATH = os.path.join(basedir, "app/static/uploads")
    LOG_LEVEL = logging.INFO

    UPLOAD_EXTENSIONS = ['.jpg', '.png']
    MAX_CONTENT_LENGTH = 1024 * 1024 * 5

    OCR_LANGUAGE = ['ch_sim', 'en']   # easyocr supported languages
    # OCR_MARKS = "!()-[]{};:'"\,<>./?@#$%^&*_~，。；、（）！”“：【】「」"
    OCR_GPU = False                   # easyocr use GPU or not


class DevelopmentConfig(BaseConfigs):
    DEBUG = True
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/ocrRecog.db' % os.getcwd()

    # celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'



    def __repr__(self):
        return '<Config for Local develop>'


class ProductionConfig(BaseConfigs):
    pass

    def __repr__(self):
        return '<Config for Product>'


class TestingConfig(BaseConfigs):

    LOG_LEVEL = logging.DEBUG

    def __repr__(self):
        return '<Config for Testing>'


ENV = os.environ.get('OCR_SERVER_CONFIG')
if ENV == 'test':
    CONFIG = TestingConfig
elif ENV == 'pro':
    CONFIG = ProductionConfig
else:
    CONFIG = DevelopmentConfig
