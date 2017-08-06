# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-05 18:06:17
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-08-06 18:56:43
"""
zh-CN:
    导出的核心流程。导出的流程是
    连接mongodb并且获取集合所有的结果 -> 结果清洗过滤校验(比如只选择某些内容) -> 将json转化为有行列的关系结构 -> 写入结果
    通过集成base_etl, 重写这个步骤中的任何一个过程，可以扩展整个导出的功能。比如说，导出为csv和导出为sql,
    实际上只是重写了 写入结果 这个方法而已。
en:
    core framework in export, export steps are:
    connection to mongodb and get all result with the specify query command ->
    filter and verify the result you get ->
    convert complex json result to table result and keep the hierarchy ->
    wirte down the result

    you can overwrite every step in this framework by inherit class base_etl. in face, export to
    csv and export to sql, just implements by overwritten the save_all_sheet_result method
"""
import argparse
from mongo_2_csv import mongo_2_csv
from mongo_2_sql import mongo_2_sql


class py_mongo_export(object):

    def parse_cmd(self):

        parser = argparse.ArgumentParser(
            description="a mongo export tool that can export 2 csv & sql")
        parser.add_argument(
            "-mongo-url", help="mongodb connection with url's format", default="mongodb://127.0.0.1:27017/")
        parser.add_argument("-d", "--db", help="database to use")
        parser.add_argument("-c", "--collection", help="collection to use")

        parser.add_argument("-lp", "--level-separator", default="~", help="level separator to connect each level filed")

        # export to csv
        parser.add_argument("-csv-file", help="ouput csv file name")
        parser.add_argument(
            "-split", help="the split symbol use in csv", default=",")

        # export to sql
        parser.add_argument("-sql-table", help="insert sql table")
        parser.add_argument("-sql-file", help="output sql script file")

        return parser

    def run(self):
        parser = self.parse_cmd()
        args = parser.parse_args()

        if args.csv_file:
            mongo_2_csv().run(args)

        if args.sql_file:
            mongo_2_sql().run(args)


if __name__ == '__main__':
    py_mongo_export().run()
