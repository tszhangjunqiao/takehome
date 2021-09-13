#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
import logging
import logging.handlers
from config import CONFIG as conf

def logger(log_path, log_level):
    if not os.path.exists(log_path):
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        with open(log_path, 'a') as f:
            pass
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    file_handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=100 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(log_level)
    formatter = logging.Formatter(
        '[%(asctime)s]-[%(threadName)s:]-[%(levelname)5s] ### %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


gLogger = logger(conf.LOG_PATH, conf.LOG_LEVEL)
