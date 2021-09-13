#!/usr/bin/env python
# -*-coding:utf-8-*-

import hashlib
import os


def md5_str(word):
    if isinstance(word, str):
        word = word.encode('utf-8')
    m = hashlib.md5()
    m.update(word)

    return m.hexdigest()


def md5_file(file_path):
    m = hashlib.md5()

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                m.update(byte_block)
    else:
        return None

    return m.hexdigest()


def get_url_file_md5(url):

    return ""

def get_url_file_name(url):
    return ""