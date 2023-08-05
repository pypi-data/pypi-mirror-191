# -*- coding: utf-8 -*-

import os


def exists_file(file_name, default=''):
    if not os.path.exists(file_name) or not os.path.getsize(file_name):
        write_file(file_name, default)
        return False

    return True


def write_file(file_name, data='', method='w'):
    with open(file_name, method, encoding='utf-8') as f:
        f.write(data)


def read_file(file_name, default=''):
    data = ''
    if exists_file(file_name, default):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()

    return data


def get_file_line(file_name):
    return read_file(file_name).splitlines()


def set_file_line(file_name, data):
    write_file(file_name, '\n'.join(data), 'w+')
