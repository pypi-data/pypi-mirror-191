# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's database connect type
"""


from typing import Any, List, Dict, Iterable, Optional, Literal, Union
import re
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine, Connection
from sqlalchemy.engine.cursor import LegacyCursorResult
from sqlalchemy.sql.elements import TextClause

from .rbasic import get_first_notnull, is_iterable, error
from .rdata import to_table, to_df, to_sql, to_csv, to_excel
from .rtext import rprint


def monkey_patch_more_fetch() -> None:
    """
    Add more methods to LegacyCursorResult object of sqlalchemy package.
    """

    # Fetch SQL result to table in List[Dict] format.
    LegacyCursorResult.fetch_table = to_table

    # Fetch SQL result to DataFrame object.
    LegacyCursorResult.fetch_df = to_df

    # Fetch SQL result to SQL syntax.
    LegacyCursorResult.fetch_sql = to_sql

    # Fetch SQL result to save csv format file.
    LegacyCursorResult.fetch_csv = to_csv

    # Fetch SQL result to save excel file.
    LegacyCursorResult.fetch_excel = to_excel

monkey_patch_more_fetch()

class RConn(object):
    """
    Rey's database connect type.
    """

    # Values to be converted to None.
    none_values: List = ["", " ", b"", [], (), {}, set()]
    
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        database: Optional[str] = None,
        charset: Optional[str] = None,
        once: bool = True,
        conn: Optional[Union[Engine, Connection]] = None
    ) -> None:
        """
        Set database connect parameters.
        """

        if type(conn) == Connection:
            conn = conn.engine
        if type(conn) == Engine:
            user = get_first_notnull(user, conn.url.username)
            password = get_first_notnull(password, conn.url.password)
            host = get_first_notnull(host, conn.url.host)
            port = get_first_notnull(port, conn.url.port)
            database = get_first_notnull(database, conn.url.database)
            charset = get_first_notnull(charset, conn.url.query.get("charset"))
            conn = conn.connect(close_with_result=once)
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.charset = charset
        self.once = once
        self.conn = conn

    def create_conn(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        database: Optional[str] = None,
        charset: Optional[str] = None,
        once: bool = None
    ) -> Connection:
        """
        Get database connect engine.
        """

        if self.conn != None\
            and (user == None or self.conn.engine.url.username == user) \
            and (password == None or self.conn.engine.url.password == password) \
            and (host == None or self.conn.engine.url.host == host) \
            and (port == None or self.conn.engine.url.port == port) \
            and (database == None or self.conn.engine.url.database == database) \
            and (charset == None or self.conn.engine.url.query["charset"] == charset):
            return self.conn

        user: str = get_first_notnull(user, self.user, default="error")
        password: str = get_first_notnull(password, self.password, default="error")
        host: str = get_first_notnull(host, self.host, default="error")
        port: Union[str, int] = get_first_notnull(port, self.port, default="error")
        database: str = get_first_notnull(database, self.database, default="error")
        charset: str = get_first_notnull(charset, self.charset, default="utf8")
        once: str = get_first_notnull(once, self.once, default=True)

        try:
            url = f"mysql+mysqldb://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        except ModuleNotFoundError:
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
            engine = create_engine(url)
        conn = engine.connect(close_with_result=once)
        if self.conn == None and not once:
            self.conn = conn
        return conn
    
    def fill_sql_none(
        self,
        sql: Union[str, TextClause],
        parms: Union[Dict, List[Dict]],
        fill_field: bool = True,
        none_values: List = none_values
    ) -> Union[Dict, List[Dict]]:
        """
        Fill missing parameters according to contents of sqlClause object of sqlalchemy module.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format or return of sqlalchemy.text.
        parms : Parameters set for filling sqlalchemy.text.
        fill_field : Whether fill missing fields.
        none_values : Values to be converted to None.

        Returns
        -------
        Filled parameters.
            - When parameter parms is Dict, then return Dict.
            - When parameter parms is List[Dict], then return List[Dict].
        """

        if type(sql) == TextClause:
            sql = sql.text
        pattern = "(?<!\\\):(\w+)"
        sql_keys = re.findall(pattern, sql)
        if type(parms) == dict:
            for key in sql_keys:
                if fill_field:
                    val = parms.get(key)
                else:
                    val = parms[key]
                if val in none_values:
                    val = None
                parms[key] = val
        else:
            for parm in parms:
                for key in sql_keys:
                    if fill_field:
                        val = parm.get(key)
                    else:
                        val = parm[key]
                    if val in none_values:
                        val = None
                    parm[key] = val
        return parms

    def execute(
        self,
        sql: str,
        parms: Optional[Union[List, Dict]] = None,
        database: Optional[str] = None,
        fill_field: bool = True,
        none_values: List = none_values,
        once: bool = None,
        **kw_parms: Any
    ) -> LegacyCursorResult:
        """
        Execute SQL.

        Parameters
        ----------
        sql : SQL in sqlalchemy.text format.
        parms : Parameters set for filling sqlalchemy.text.
        database : Database name.
        fill_field : Whether fill missing fields.
        none_values : Values to be converted to None.
        once : Whether the database connect engine is one-time (i.e. real time creation).
        kw_parms : Keyword parameters for filling sqlalchemy.text.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        once = get_first_notnull(once, self.once, default=True)

        conn = self.create_conn(database=database, once=once)
        if parms != None or kw_parms != {}:
            if parms != None and kw_parms != {}:
                if type(parms) == list:
                    for parm in parms:
                        parm.update(kw_parms)
                else:
                    parms.update(kw_parms)
            elif kw_parms != {}:
                parms = kw_parms
            if parms != None:
                parms = self.fill_sql_none(sql, parms, fill_field, none_values)
            sql = text(sql)
            result = conn.execute(sql, parms)
        else:
            result = conn.execute(sql)
        if once:
            conn.close()
            del self.conn
            self.conn = None
        return result

    def execute_select(
            self,
            table: str,
            database: Optional[str] = None,
            fields: Optional[Union[str, Iterable]] = None,
            where: Optional[str] = None,
            order: Optional[str] = None,
            limit: Optional[Union[int, str, Iterable[Union[int, str]]]] = None,
            print_sql: bool = False
        ) -> LegacyCursorResult:
        """
        Execute select SQL.

        Parameters
        ----------
        table : Table name.
        database : Database name.
        fields : Select syntax content.
            - None : Is 'SELECT *'.
            - str : Join as 'SELECT str'.
            - Iterable[str] : Join as 'SELECT \`str\`, ...'.

        where : 'WHERE' syntax content, join as 'WHERE str'.
        order : 'ORDER BY' syntax content, join as 'ORDER BY str'.
        limit : 'LIMIT' syntax content.
            - Union[int, str] : Join as 'LIMIT int/str'.
            - Iterable[Union[str, int]] with length of 1 or 2 : Join as 'LIMIT int/str, ...'.

        print_sql : Whether print SQL.

        Returns
        -------
        LegacyCursorResult object of alsqlchemy package.
        """

        sqls = []
        if database == None:
            _database = self.database
        else:
            _database = database
        if fields == None:
            fields = "*"
        elif is_iterable(fields):
                fields = ",".join(["`%s`" % field for field in fields])
        select_sql = (
            f"SELECT {fields}\n"
            f"FROM `{_database}`.`{table}`"
        )
        sqls.append(select_sql)
        if where != None:
            where_sql = "WHERE %s" % where
            sqls.append(where_sql)
        if order != None:
            order_sql = "ORDER BY %s" % order
            sqls.append(order_sql)
        if limit != None:
            list_type = type(limit)
            if list_type in [str, int]:
                limit_sql = f"LIMIT {limit}"
            else:
                if len(limit) in [1, 2]:
                    limit_content = ",".join([str(val) for val in limit])
                    limit_sql = "LIMIT %s" % limit_content
                else:
                    error("The length of the limit parameter value must be 1 or 2", ValueError)
            sqls.append(limit_sql)
        sql = "\n".join(sqls)
        if print_sql:
            rprint(sql, title="SQL", frame="half")
        result = self.execute(sql, database=database)
        return result


    def execute_update(
        self,
        data: Union[LegacyCursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        primary_key: Optional[str] = None,
        print_sql: bool = False
    ) -> None:
        """
        Update the data of table in the datebase.
    
        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        primary_key : 'WHERE' syntax content.
            - None : Is 'WHERE `%s` = :%s' % (first field name and value of each item).
            - str : Is f'WHERE `{str}` = :{str}'.

        print_sql : Whether print SQL.
        """

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = to_table(data)
        elif data_type == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database
        for row in data:
            if primary_key == None:
                primary_key = list(row.keys())[0]
            set_content = ",".join(["`%s` = :%s" % (key, key)for key in row if key != primary_key])
            sql = (
                f"UPDATE `{_database}`.`{table}`\n"
                f"SET {set_content}\n"
                f"WHERE `{primary_key}` = :{primary_key}"
            )
            if print_sql:
                rprint(sql, title="SQL", frame="half")
            self.execute(sql, row, database, once=False)
        if self.once:
            self.conn == None

    def execute_insert(
        self,
        data: Union[LegacyCursorResult, List[Dict], Dict],
        table: str,
        database: Optional[str] = None,
        duplicate_method: Optional[Literal["ignore", "update"]] = None,
        print_sql: bool = False
    ) -> None:
        """
        Insert the data of table in the datebase.

        Parameters
        ----------
        data : Updated data.
        table : Table name.
        database : Database name.
        duplicate_method : Syntax method when constraint error.
            - None : Then no syntax.
            - 'ignore' : Is 'UPDATE IGNORE INTO'.
            - 'update' : Is 'ON DUPLICATE KEY UPDATE'.

        print_sql : Whether print SQL.
        """

        data_type = type(data)
        if data_type == LegacyCursorResult:
            data = self.to_table(data)
        elif data_type == dict:
            data = [data]
        if database == None:
            _database = self.database
        else:
            _database = database
        fields = list({key for row in data for key in row})
        fields_str = ",".join(["`%s`" % field for field in fields])
        fields_str_position = ",".join([":" + field for field in fields])
        if duplicate_method == "ignore":
            sql = (
                f"INSERT IGNORE INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        elif duplicate_method == "update":
            update_content = ",".join(["`%s` = VALUES(`%s`)" % (field, field) for field in fields])
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})\n"
                "ON DUPLICATE KEY UPDATE\n"
                f"{update_content}"
            )
        else:
            sql = (
                f"INSERT INTO `{_database}`.`{table}`({fields_str})\n"
                f"VALUES({fields_str_position})"
            )
        if print_sql:
            rprint(sql, title="SQL", frame="half")
        self.execute(sql, data, database)