#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from config import DEFAULT_CASES_DIR

cases_code = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from config import *


api = HOST_URL + {}
definitions = {}


def _get_parameters(factory, conn):
    parameters = dict()
    for k, v in definitions.items():
        m = re.search(PATTERN, v)
        if m.group(3):
            pass  # todo image url
        elif m.group(2):
            tb, col = m.group(2).split('.')
            cursor = conn.cursor()
            cursor.execute(SQL, (tb, col))
            parameters[k] = cursor.fetchone()
            conn.commit()
        else:
            parameters[k] = getattr(factory, m.group(1))
    conn.close()
    return parameters


def _get_authority():
    pass
    

"""

request_code = """
res = requests.{}(api, params=_get_parameters())
"""

config_code = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

SQL = 'SELECT %s FROM %s'
HOST_URL = {}
PATTERN = '\(([a-zA-Z_]+)\s*,?\s*([a-zA-Z_]+\.[a-zA-Z_]+)?\s*,?\s*(\w+)?\)'

host = ''
port = ''
user = ''
password = ''
db = ''
locale = ''
seed = ''

"""

env_code = """
import pymysql
from faker import Faker
from config import *


def get_factory():
    if not locale:
        factory = Faker()
    else:
        try:
            factory = Faker(locale)
        except AttributeError:  # todo log
            print('Specified locale is not supported, using en_US')
            factory = Faker()
    if seed:
        factory.seed(seed)
    return factory


def get_connection():
    return pymysql.connect(host=host,
                           port=port,
                           user=user,
                           passwd=password,
                           db=db,
                           charset='utf8',
                           use_unicode=True)

"""


def init_cases(swagger, host_url, cases_path, tags=None):
    cases_dir = _make_cases_dir(cases_path)
    _init_config_file(cases_dir, host_url)
    _init_env_file(cases_dir)
    paths = _filter_tags(swagger, tags)
    for path, info in paths.items():
        code = None
        flag = True
        tag = None
        for method_name, data in path.items():
            code_format = None
            if flag:
                definitions = {}
                if 'parameters' in paths[path][method_name]:
                    parameters = paths[path][method_name]['parameters']
                    for param in parameters:
                        definition = param['vendorExtensions'][0]['name']
                        definitions[param['name']] = definition
                code_format = cases_code.format(path, definitions)
                tag = info[tags][0]
                flag = False
            code = code_format + request_code.format(method_name)
        case_file_name = cases_dir + tag + '_'.join(path.split('/')[1:])
        with open(case_file_name, 'w+', encoding='utf-8') as f:
            f.write(code)


def _make_cases_dir(cases_path):
    cwd = os.getcwd()
    if cases_path:
        if os.path.isabs(cases_path):
            path = cases_path
            os.makedirs(cases_path, exist_ok=True)
        else:
            path = cwd + cases_path
            os.makedirs(path, exist_ok=True)
    else:
        path = cwd + DEFAULT_CASES_DIR
        os.makedirs(path, exist_ok=True)
    return path


def _init_config_file(cases_dir, host_url):
    file_path = cases_dir + '/config.py'
    with open(file_path, 'w+', encoding='utf-8') as f:
        f.write(config_code.format(host_url))


def _init_env_file(cases_dir):
    file_path = cases_dir + '/env.py'
    with open(file_path, 'w+', encoding='utf-8') as f:
        f.write(env_code)


def _filter_tags(swagger, tags):
    if not tags:
        return swagger['paths']
    paths = {}
    for path, info in swagger['paths'].items():
        method = next(iter(info.values()))
        for tag in method['tags']:
            if tag in tags:
                paths[path] = info
                break
    return paths
