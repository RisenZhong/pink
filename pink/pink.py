#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import requests
from antlr4 import FileStream
import api_case
from mysql_faker import MySqlFaker


usage = """
Usage:
  pink <command> [options]

Commands:
  fill                        Fill database.
  api                         Generate api case files.
  doc                         Generate db doc files.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  -v, --verbose               Give more output. Option is additive, and can be
                              used up to 3 times.
  -V, --version               Show version and exit.
  
Fill Options:
  -t                          Database type. Default is MySQL.
  -f                          Sql file.
  -i                          Database host.
  -o                          Database port.
  -n                          Database name.
  -u                          Database username.
  -p                          Database password.
  -r                          Data num(rows).

Api Options:
  -p                          Api path.
  -d                          Generated files stored path.
  
Doc Options:
  -f                          Sql file.
  -d                          Generated files stored path.
"""


def fill_data(ns):
    if not ns.type or ns.type.lower() == 'mysql':
        stream = FileStream(ns.sql)
        faker = MySqlFaker(host=ns.host,
                           port=ns.port,
                           user=ns.username,
                           password=ns.password,
                           db=ns.database)

        faker.save_to_db(stream, ns.num)
    else:
        raise ValueError('Database type not support yet.')


def generate_api_cases(ns):
    swagger_url_path = '/v2/api-docs'
    res = requests.get(ns.path + swagger_url_path)
    if res.status_code != 200:
        raise ValueError('Can not connect to api server.')
    api_case.init_cases(res.json(), ns.path, ns.dir)


def generate_db_doc(ns):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Pink')
    subparsers = parser.add_subparsers()

    # fill command
    parser_fill = subparsers.add_parser('fill', help='fill help')
    parser_fill.add_argument('-t', dest='type')
    parser_fill.add_argument('-f', dest='sql')
    parser_fill.add_argument('-i', dest='host')
    parser_fill.add_argument('-o', dest='port')
    parser_fill.add_argument('-n', dest='database')
    parser_fill.add_argument('-u', dest='username')
    parser_fill.add_argument('-p', dest='password')
    parser_fill.add_argument('-m', dest='num')
    parser_fill.set_defaults(func=fill_data)

    # api command
    parser_api = subparsers.add_parser('api', help='api help')
    parser_api.add_argument('-p', dest='path')
    parser_api.add_argument('-d', dest='dir')
    parser_api.set_defaults(func=generate_api_cases)

    # doc command
    parser_doc = subparsers.add_parser('doc', help='doc help')
    parser_doc.add_argument('-f', dest='sql')
    parser_doc.add_argument('-d', dest='dir')
    parser_doc.set_defaults(func=generate_db_doc)

    args = parser.parse_args()
    args.func(args)
