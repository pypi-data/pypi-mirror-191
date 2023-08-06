#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Common Runtime CRUD Operations """


from typing import List

from psycopg2.extensions import connection

from baseblock import BaseObject


class PerformRuntimeCrud(BaseObject):
    """ Perform Common Runtime CRUD Operations """

    def __init__(self,
                 conn: connection):
        """ Change Log

        Created:
            16-Nov-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self.conn = conn

    def read(self,
             sql: str) -> list:

        results = []

        try:

            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    results.append(row)

        except Exception as err:
            self.logger.error(err)
            raise ValueError(sql)

        return results

    def delete(self,
               sql: str, *args) -> None:
        try:

            with self.conn.cursor() as cursor:
                cursor.execute(sql, list(args))
                self.conn.commit()

        except Exception as err:
            self.logger.error(err)
            raise ValueError(sql)

    def insert(self,
               schema_name: str,
               table_name: str,
               column_names: List[str],
               column_values: List[str]) -> None:
        """ Insert Data

        Args:
            schema_name (str): the schema name
            table_name (str): the table name
            args (*): any values to insert

        Raises:
            ValueError: _description_
        """

        def tostr(values: List[str]) -> str:
            return f"({', '.join([x for x in values])})"

        def todqots(values: List[str]) -> str:
            return f"({', '.join(['%s' for x in values])})"

        insert_query = f"INSERT INTO {schema_name}.{table_name} #names VALUES #values"
        insert_query = insert_query.replace('#names', tostr(column_names))
        insert_query = insert_query.replace('#values', todqots(column_values))

        try:

            with self.conn.cursor() as cursor:
                cursor.execute(insert_query, column_values)
                self.conn.commit()

        except Exception as err:
            self.logger.error(err)
            raise ValueError(insert_query)
