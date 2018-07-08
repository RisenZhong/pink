#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from antlr4 import *
from database import Database
from base_faker import BaseFaker
from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser
from database_listener import DatabaseListener
from parser import Parser


class MySqlFaker(BaseFaker):

    def __init__(self, host, port, user, password, db):
        super().__init__()
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    passwd=password,
                                    db=db,
                                    charset='utf8',
                                    use_unicode=True)

    def get_database(self, input_stream):
        database = Database(self.conn.db)
        lexer = MySqlLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MySqlParser(stream)
        tree = parser.root()

        listener = DatabaseListener(database)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.database

    def fill_database(self, input_stream, num):
        database = self.get_database(input_stream)
        self.fill_parent_columns(database, num)
        for tb in database.tables:
            for col in tb.columns:
                for i in range(num):
                    val = Parser().get_provider(col.pink_def)
                    col.values.append(val)
        return database

    def fill_parent_columns(self, database, num):
        for key, pc in database.parent_columns.items():
            for i in range(num):
                val = getattr(self.factory, pc.faker_type)
                database.parent_columns.append(val)

    def save_to_db(self, input_stream, num):
        database = self.fill_database(input_stream, num)
        sql_list = []
        sql = 'INSERT INTO '
        for tb in database.tables:
            sql += (tb.name + '(')
            column_names = list(map(lambda c: c.name, tb.columns))
            sql += ','.join(column_names) + ') VALUES'
            values = []

            for i in range(len(tb.columns.values)):
                item = []
                for col in tb.columns:
                    item.append(col.values[i])
                e = '(' + ','.join(item) + ')'
                values.append(e)
            sql += ','.join(values)
        sql_list.append(sql)

        cursor = self.conn.cursor()
        for sql in sql_list:
            cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
