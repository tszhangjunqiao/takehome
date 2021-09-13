from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

import os

from app import ocrer
from app.models import *
from app.app_util import *
from utils.md5 import md5_file
from utils.logger import gLogger

# from app.extensions import celery
from server import celery_app as celery


@celery.task(bind=True)
def ocr_task(self, absolute_path):
    # 异步处理
    print("celery ocr_task")
    results = None
    filename = os.path.basename(absolute_path)
    try:
        md5 = md5_file(absolute_path)
    except Exception as e:
        md5 = None
        gLogger.error("calculate md5 error: {}".format(e))

    self.update_sate(state="PROCESS")
    # save file to FileUpload table
    try:
        file_upload = FileUpload.query.filter_by(file_md5=md5).first()
        if not file_upload:
            file_upload = FileUpload(file_name=filename, file_path=absolute_path, file_md5=md5)
            db.session.add(file_upload)
        else:
            file_upload.file_name = filename
            file_upload.file_path = absolute_path
            file_upload.timestamp = datetime.datetime.now()

        # get ocr result and save to database
        md5_result = Results.get_db_ocr_result(md5)
        if md5_result:
            results = md5_result.ocr_results.get('content')
        else:
            results = ocrer.get_ocr_result(absolute_path)

            # save result to database
            res = Results(file_md5=md5, ocr_results=build_ocr_data(results))
            db.session.add(res)

        db.session.commit()

        self.update_sate(state="SUCCESS")
        return build_ocr_data(results)

    except IntegrityError as e:
        db.session.rollback()
        gLogger.error("{}".format(e))
        self.update_sate(state="FAILED")

    return build_ocr_data(results)



