# coding=utf-8
"""Koskya Utilities Module
contains the Kosakya Human Friendly Classes
"""

import re
from humanfriendly import format_size as HFformat_size
from humanfriendly import parse_size as HFparse_size


class HF:
    """Human Friendly Formatting Class
    """

    @staticmethod
    def format_size(size, suffix='IEC'):
        return HFformat_size(size, binary=True)
        if suffix == 'IEC':
            return HFformat_size(size, binary=True)
        return HFformat_size(size)

    @staticmethod
    def parse_size(size):
        p = re.compile(r'[EPTGMK]iB', re.IGNORECASE)
        if p.match(size):
            return HFparse_size(size, binary=True)
        return HFparse_size(size)
