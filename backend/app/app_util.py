
import imghdr
from flask import make_response, jsonify

from app.api import api
from config import CONFIG


def validate_image_format(img_stream):
    """
    checke image format
    :param img_stream:
    :return:
    """
    header = img_stream.read(512)
    img_stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def ResponseError(msg, code):
    return make_response(jsonify({
        "msg": msg,
        "data": None
    }),
        code
    )

def ResponseData(data, code):
    return make_response(jsonify({
        "msg": "ok",
        "data": data
    }),
        code
    )


@api.errorhandler(413)
def too_large(e):
    return ResponseError("File is too large, should less than %dM"
                         % (int(CONFIG.MAX_CONTENT_LENGTH) / 1024 / 1024), 413)


def build_ocr_data(results):
    return {
        "content": results
    }