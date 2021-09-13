
from utils.ocr import OCRer
from config import CONFIG

from celery import Celery, Task

from app import create_app, make_celery


app = create_app()
celery_app = make_celery(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG.PORT, debug=CONFIG.DEBUG)
