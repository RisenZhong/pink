#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from database import *
from MySqlParser import MySqlParser
from mysql.MySqlParserListener import MySqlParserListener


pattern = '\(([a-zA-Z_]+)\s*,?\s*([a-zA-Z_]+\.[a-zA-Z_]+)?\s*,?\s*(\w+)?\)'


class DatabaseListener(MySqlParserListener):

    def __init__(self, database):
        self.database = database

    def exitColumnCreateTable(self, ctx: MySqlParser.ColumnCreateTableContext):
        table_name = ''
        columns = []
        for c in ctx.getChildren():
            if type(c) is MySqlParser.TableNameContext:
                table_name = c.getText()
            if type(c) is MySqlParser.CreateDefinitionsContext:
                self.resolve_create_definitions_context(c, columns)
        self.database.tables.append(Table(table_name, columns))

    def resolve_create_definitions_context(self, ctx: MySqlParser.CreateDefinitionsContext, columns):
        for c in ctx.getChildren():
            if type(c) is MySqlParser.ColumnDeclarationContext:
                self.resolve_column_declaration_context(c, columns)
            if type(c) is MySqlParser.ConstraintDeclarationContext:
                pass
            if type(c) is MySqlParser.IndexDeclarationContext:
                pass

    def resolve_column_declaration_context(self, ctx: MySqlParser.ColumnDeclarationContext, columns):
        column = Column()
        for c in ctx.getChildren():
            if type(c) is MySqlParser.UidContext:
                column.name = c.getText()
            if type(c) is MySqlParser.ColumnDefinitionContext:
                self.resolve_column_definition_context(c, column)
        columns.append(column)

    def resolve_column_definition_context(self, ctx: MySqlParser.ColumnDefinitionContext, column):
        for c in ctx.getChildren():
            if isinstance(c, MySqlParser.DataTypeContext):
                column.type = c.getText()
            if type(c) is MySqlParser.NullColumnConstraintContext:
                column.not_null = True
            if type(c) is MySqlParser.CommentColumnConstraintContext:
                self.resolve_comment_column_constraint_context(c, column)

    def resolve_comment_column_constraint_context(self, ctx: MySqlParser.CommentColumnConstraintContext, column):
        comment = ctx.getChildren()[1].getText()
        m = re.search(pattern, comment)
        faker_type = m.group(1)
        if not faker_type:
            pass  # todo exception
        else:
            column.faker_type = faker_type
        parent_column = m.group(2)
        if parent_column:
            parent_columns = self.database.parent_columns
            if parent_column in parent_columns:
                column.parent_column = parent_columns[parent_column]
            else:
                pc = ParentColumn()
                pc.name = parent_column
                pc.faker_type = column.faker_type
                column.parent_column = pc
                parent_columns[parent_column] = pc


