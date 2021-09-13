#!/usr/bin/env python
# -*-coding:utf-8-*-

import easyocr

from utils.logger import gLogger


class OCRer(object):
    def __init__(self, languages: list, gpu: bool, *args):
        self.reader = easyocr.Reader(languages, gpu=gpu, *args)

    def get_ocr_result(self, image):
        """

        :param image:  图片的绝对路径或者url, 或者二进制图像数据
        :return:  返回一个列表，A list contains all splitted letters exclude punctuation
        """
        split_res = None
        try:
            results = self.reader.readtext(image)
            print(results)
            res = self._parse_results(results)
            split_res = self._split_letters(res)
        except Exception as e:
            gLogger.error("OCRer get_ocr_result error: {}".format(e))

        return split_res

    def _parse_results(self, results):
        """

        :param results:
        :return:
        """
        texts = [res[1] for res in results if len(res) >= 2]
        return "".join(texts)

    def _split_letters(self, texts):
        """

        :param texts:
        :return:
        """
        letters = texts.strip().replace(" ", "")
        marks = r'''!()-[]{};:'"\,<>./?@#$%^&*_~，。；、（）！”“：【】「」'''

        res = [ letter for letter in letters
                if letter not in marks
              ]

        # print(res)

        return res


if __name__ == '__main__':
    ocr = OCRer(['ch_sim', 'en'], False)
    # print(ocr.get_ocr_result("C:\\Users\\hyjun\\Pictures\\20210910093650.png"))
    f = open("C:/Users/hyjun/Pictures/road_ch_en.jpg", 'rb')
    import base64
    img = base64.b64encode(f.read())
    print(len(img))
    # print(ocr.get_ocr_result(base64.b64decode(img)))
    # print(ocr.get_ocr_result("C:/Users/hyjun/Pictures/road_ch_en.jpg"))
    print(ocr.get_ocr_result("http://jeroen.github.io/images/testocr.png"))