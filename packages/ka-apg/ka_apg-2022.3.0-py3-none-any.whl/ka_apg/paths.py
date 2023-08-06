# coding=utf-8
"""Koskya Utilities Module
contains the Kosakya Utilitiy Classes
"""

from ka_utg.dod import DoD as KaDoD
from ka_utg.file import File as KaFile
from .path import Path as KaPath


class Paths:

    @staticmethod
    def get(paths=None, keys=None, prefix=None):
        """get path from nested dictionary of paths
        get the path from the nested path dictionary by looping through
        the keys list and recursively locating the dictionary value
        for every key

        Args:
            paths (dict): dictionary of paths
            keys (list): array of keys
            path_prefix (str): path prefix
        Returns:
            path (str): path
        """
        return KaPath.get(KaDoD.get_item_(paths, keys), prefix)

    @classmethod
    def read(cls, paths=None, keys=None, prefix=None, sw_warning=False):
        """get path from nested dictionary of paths and read path

        Args:
            paths (dict): dictionary of paths
            keys (list): array of keys
            path_prefix (str): path prefix
        Returns:
            (list): File content
        """
        return KaFile.read(cls.get(paths, keys, prefix), sw_warning)
