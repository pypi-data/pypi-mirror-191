"""
pip install -U pyxk -i https://pypi.org/simple
"""
from pyxk.aes import Cryptor
from pyxk.m3u8 import M3U8
from pyxk.requests import (
    Session,
    delete,
    get, head,
    options,
    patch,
    post,
    put,
    request)
