from app import db
import datetime


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)


class FileUpload(BaseModel):
    """
    存上传的文件信息
    """
    __tablename__ = 'file_upload'

    file_name = db.Column(db.String(256), nullable=False)
    file_path = db.Column(db.String(256), nullable=True)
    file_md5 = db.Column(db.String(128), index=True, nullable=False, unique=True)
    file_url = db.Column(db.String(256), nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    @staticmethod
    def is_file_exists(file_md5):
        if FileUpload.query.filter_by(file_md5=file_md5).first():
            return True
        else:
            return False


class Tasks(BaseModel):
    """
    存每一次提交的ocr任务
    """
    __tablename__ = "tasks"

    task_id = db.Column(db.String(128), unique=True, nullable=False)
    file_md5 = db.Column(db.String(128), nullable=False)
    task_state = db.Column(db.String(64), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())


class Results(BaseModel):
    """
    保存图片md5及对应的ocr识别结果，多次提交的任务可能对应一条结果。 因为md5值相同，那么没必要重新识别
    """
    __table__name = 'results'

    file_md5 = db.Column(db.String(128), nullable=False, unique=True)
    ocr_results = db.Column(db.JSON, nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    @staticmethod
    def get_db_ocr_result(md5):
        return Results.query.filter_by(file_md5=md5).first()

