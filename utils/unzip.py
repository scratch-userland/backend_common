# -*- coding: utf-8 -*-

import zipfile


def unzip(filename, folder=None):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(filename)
    for names in zip_file.namelist():
        zip_file.extract(names, folder)
    zip_file.close()
