# -*- coding: utf-8 -*-

import os


def list_dir(dir):
    new_dir = []
    for name in os.listdir(dir):
        if name == '.DS_Store' or name == '.' or name == '..':
            continue

        new_dir.append(name)

    return new_dir
