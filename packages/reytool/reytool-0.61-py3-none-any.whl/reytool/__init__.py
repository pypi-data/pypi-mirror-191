# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:21
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's personal tool set
"""


from .remail import REmail
from .rdatabase import RConn
from .rdata import count, flatten, split
from .rbasic import error, warn, de_duplicate
from .rcommon import exc, digits, randn, sleep, get_paths
from .rwrap import runtime
from .rtime import RTMark, now
from .rtext import rprint
from .rrequest import request
from .rtranslate import translate
from .rregular import res
from .rzip import azip