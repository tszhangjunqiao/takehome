#!/usr/bin/env python
# -*-coding:utf-8-*-
import datetime

from flask import Flask, render_template, request, redirect, url_for, abort
from flask import make_response, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

import os
import json

from app.api import api
from app.app_util import *
from app import ocrer, db
from app.models import *
from app.tasks import ocr_task

from config import CONFIG
from utils.md5 import md5_file, get_url_file_name, get_url_file_md5
from utils.logger import gLogger


@api.route('/')
def index():
    return "index"


@api.route('/ocr_recognize', methods=["POST"])
def ocr_recognize():
    """
    md5相同或url相同的图片，可能多个用户上传同一张图片（文件名不同,但md5相同）,此时可以直接返回以前的计算结果。

    :return:
    """
    if request.method == 'POST':
        upload_url = request.form.get('url')
        uploaded_file = request.files.get('image')

        if uploaded_file:
            # 处理传入multipart/form-data 的情况
            filename = secure_filename(uploaded_file.filename)

            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in CONFIG.UPLOAD_EXTENSIONS or file_ext != validate_image_format(uploaded_file.stream):
                    return ResponseError("not supported image format", 400)

                absolute_path = os.path.join(CONFIG.UPLOAD_PATH, filename)
                uploaded_file.save(absolute_path)
                print("start orc_task...")
                task = ocr_task.delay(absolute_path)

                return ResponseData({"task_id": task.id}, 202)

                # uploaded_file.save(absolute_path)
                # md5 = md5_file(absolute_path)
                #
                # # save file to FileUpload table
                # try:
                #     file_upload = FileUpload.query.filter_by(file_md5=md5).first()
                #     if not file_upload:
                #         file_upload = FileUpload(file_name=filename, file_path=absolute_path, file_md5=md5)
                #         db.session.add(file_upload)
                #     else:
                #         file_upload.file_name = filename
                #         file_upload.file_path = absolute_path
                #         file_upload.timestamp = datetime.datetime.now()
                #
                #     # get ocr result and save to database
                #     md5_result = Results.get_db_ocr_result(md5)
                #     if md5_result:
                #         print(type(md5_result))
                #         results = md5_result.ocr_results.get('content')
                #     else:
                #         results = ocrer.get_ocr_result(absolute_path)
                #
                #         # save result to database
                #         res = Results(file_md5=md5, ocr_results=build_ocr_data(results))
                #         db.session.add(res)
                #     db.session.commit()
                #
                # except IntegrityError as e:
                #     db.session.rollback()
                #     gLogger.error("{}".format(e))
                #     return ResponseError('Add upload file {} failed, please try it again'.format(filename), 500)
                #
                # return make_response(jsonify(build_ocr_data(results)), 200)

        # elif upload_url:
            # 处理传入url的情况
            # get url image md5
            # md5 = get_url_file_md5(upload_url)
            # filename = get_url_file_mame(upload_url)
            # absolute_path = os.path.join(CONFIG.UPLOAD_PATH, filename)
            #
            # file_upload = FileUpload.query.filter_by(file_url=upload_url).first()
            # if not file_upload:
            #     file_upload = FileUpload(file_name=filename, file_path=absolute_path, file_md5=md5)
            #     db.session.add(file_upload)
            # else:
            #     file_upload.file_url = upload_url
            #     file_upload.timestamp = datetime.datetime.now()
            #
            # # get ocr result and save to database
            # md5_result = Results.get_db_ocr_result(md5)
            # if md5_result:
            #     print(type(md5_result))
            #     results = md5_result.ocr_results.get('content')
            # else:
            #     results = ocrer.get_ocr_result(os.path.join(CONFIG.UPLOAD_PATH, filename))
            #     # save result to database
            #     res = Results(file_md5=md5, ocr_results=build_ocr_data(results))
            #     db.session.add(res)
            # db.session.commit()
            #
            # return ResponseData(build_ocr_data(results), 200)

        else:
            return ResponseError("post params wrong.", 400)

    else:
        return ResponseError("Only support POST method", 400)


@api.route('/status/<task_id>')
def task_status(task_id):
    # 获取异步任务结果
    task = ocr_task.AsyncResult(task_id)
    # 等待处理
    if task.state == 'PENDING':
        response = {'state': task.state}
    elif task.state != 'FAILURE':
        response = task.info
    else:
        # 后台任务出错
        response = {'state': task.state}
    return ResponseData(response, 200)