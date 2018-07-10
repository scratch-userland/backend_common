# -*- coding: utf-8 -*-
import os
import shutil
import zipfile


def unzip(filename, folder=None):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(filename)
    for names in zip_file.namelist():
        zip_file.extract(names, folder)
    zip_file.close()


def mkdirs(path):
    upperdirs = os.path.dirname(path)
    if upperdirs and not os.path.exists(upperdirs):
        os.makedirs(upperdirs)


def get_upper_dir(path):
    upperdirs = os.path.dirname(path)
    return upperdirs


def copyfiles(source, dest):
    """
    拷贝文件或目录
        source可以为文件或者目录
    """
    if not os.path.exists(source):
        raise Exception(u'源文件不存在!')

    if os.path.isdir(source):  # 如果源文件是目录
        # 如果dest存在,先删除
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(source, dest)
    else:
        # 确认dest文件的所有上级目录存在
        mkdirs(dest)
        shutil.copyfile(source, dest)


def renamefile(source, dest):
    """
    文件重命名
    """
    os.rename(source, dest)


def list_files_in_dir(dir_path):
    """
    返回目录下的所有文件名和绝对路径
    [
        {
           "key": "file name",
            "path": "abs path"
        },
        ...
    ]

    """
    lists = []
    for f in os.listdir(dir_path):
        f_path = os.path.join(dir_path, f)
        if os.path.isfile(f_path):
            lists.append({
                'key': f,
                'path': f_path
            })
    return lists
