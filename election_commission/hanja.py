#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

import re

__all__ = ['name_cn_re']

HANJA_RANGES = [[0x2E80, 0x2FD5],
                [0x3005, 0x32FF],
                [0x3400, 0x4DBF],
                [0x4E00, 0x9FC3],
                [0xF900, 0xFAFF],
                [0x20000, 0x2A6DF],
                [0x2F800, 0x2FA1F]]

def build_re():
    hangul = 'ㄱ-ㅎ가-힣'
    hanja = ''.join('%s-%s' % (chr(f), chr(t)) for (f, t) in HANJA_RANGES)
    special_chars = r'\s'
    regexp = '[%s%s%s]+$' % (hangul, hanja, special_chars)
    return re.compile(regexp, re.UNICODE)

name_cn_re = build_re()
