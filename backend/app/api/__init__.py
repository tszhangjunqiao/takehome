from flask import Blueprint

# 两个参数分别指定蓝本的名字、蓝本所在的包或模块
api = Blueprint('api', __name__)

from app.api import routes