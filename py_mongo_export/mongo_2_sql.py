# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-07-18 17:41:28
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-08-05 23:21:26

import logging
from base_etl import base_etl
from DBService import MysqlService

logger = logging.getLogger(__name__)


class mongo_2_sql(base_etl):

    def save_all_sheet_result(self, valid_sheet_result, args):
        table, sql_file = args.sql_table, args.sql_file
        create_table_sql = self.create_table_sql(table, valid_sheet_result)
        content_sql = self.create_content_sql(table, valid_sheet_result)
        with open(sql_file, "w") as f:
            f.write(create_table_sql)
            f.write("\n".join(content_sql))

    def create_table_sql(self, table, result_sheets):
        fields = set()
        for result in result_sheets:
            for k in result.keys():
                fields.add(k)
        fields = list(fields)
        # 开始构造建表sql
        sql_head = "create table %s(\n" % table
        sql_foot = "\n)engine=InnoDB charset utf8;\n"
        sql_content = ",\n".join(["`%s` text" % f for f in fields])
        return sql_head + sql_content + sql_foot

    def create_content_sql(self, table, result_sheets):
        content_sql = []
        for result in result_sheets:
            sql = MysqlService.join_sql_from_map(table, result)
            content_sql.append(sql)
        return content_sql


if __name__ == '__main__':
    mongo_2_mysql().run()
