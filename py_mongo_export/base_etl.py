# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-07-18 16:11:45
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-08-06 18:56:55

import logging
from DBService import MongoService

logger = logging.getLogger(__name__)

class base_etl(object):

    def run(self, args):
        # step_1 : get all result in collection
        logger.info("start connect mongo & get result")
        mongo_result = self.get_mongo_all_result(args.mongo_url, args.db, args.collection)

        # step_2: filter and verify mongo result
        logger.info("get mongo data successed, get %d mongo result, now start clean mongo result" % len(mongo_result))
        valid_result = self.parse_mongo_result(mongo_result)

        # step_3: convert mongo result to table
        logger.info("clean mongo result successed, now mongo result count is %d, now start convert mongo result -> sheet" % len(valid_result))
        valid_sheet_result = [self._convert_mongo_2_sheet(result, args.level_separator, filter_callback=self.filter_sheet).copy() for result in valid_result]

        # save all result
        logger.info("start save all mongo result")
        self.save_all_sheet_result(valid_sheet_result, args)
        logger.info("all successed !")

    def mongo_server_check(self, mongo_url, mongo_db_name):
        """
        检查是否已经有mongo连接, 在多次调用函数的时候避免每次重新连接mongodb
        返回的是直接可以用的mongo server，直接用mongo server去查询
        如果有，检查是否连接地址和库是否都一样，都一样，不用操作
        如果有，连接地址一样，数据库地址不一样，那么更新self.mongo_server的库就行了
        如果都不对，或者压根没有mongo_server，那么就要重新保存mongo_server
        """

        # 如果已经有了mongo的连接
        if hasattr(self, "mongo_server"):
            # 如果连接地址和库都一样，那么就可以使用之前的连接
            if mogno_url == self.mogno_url and mongo_db_name == self.mongo_db_name:
                return self.mongo_server
            # 如果只是连接地址不一样，那么还好可以过来，不需要重新连接
            elif mongo_url == self.mongo_url and mongo_db_name != self.mongo_db_name:
                self.mongo_server.select_db(mongo_db_name)
                return self.mongo_server
        # 如果没有连接，或者连接两个都不对都没有进去return
        self.mongo_server = MongoService(mongo_url)
        self.mongo_server.select_db(mongo_db_name)
        # 然后保存最新的mongo的连接地址和连接库
        self.mongo_url, self.mongo_db_name = mongo_url, mongo_db_name
        return self.mongo_server

    def get_mongo_all_result(self, mongo_url, mongo_db_name, collection):
        """抽取mongodb中指定collections的全部数据 """
        server = self.mongo_server_check(mongo_url, mongo_db_name)
        return server.find_all(collection, {})

    def get_mongo_result_limit(self, mongo_url, mongo_db_name, collection, limit=50):
        """只抽取部分结果，加快速度方便debug """
        server = self.mongo_server_check(mongo_url, mongo_db_name)
        return server.find_limit(collection, limit)

    def parse_mongo_result(self, mongo_result):
        """
        这个函数子类可以覆盖，来达到个性化解析mongodb内容的效果
        默认情况是，是只提取mongo里面的url字段，并且不做处理直接插入
        一种虽然只需要url字段但是需要处理的情况是：url某个字段错了，需要批量替换
        """
        # 都需要去除_id字段
        # map(lambda result: result.pop("_id"), mongo_result)
        return mongo_result

    def _convert_mongo_2_sheet(self, document, interval, prefix=[], result={}, filter_callback=(lambda x: True)):
        """
        zh-CN:
            通过DFS递归把多层的dict平铺，去掉层级关系，层级前缀用 interval 连接
            回调一个过滤函数，在是字典类型的时候开始调用，方便指定不添加哪些(哪一层)字段，不然平铺出来的字段会无限扩充
        en: use DFS(recursion) to convert complex, multi level json document to
        single level table document. and call back a filter function to limit didn't add which field

        """
        if isinstance(document, dict):
            for k, v in document.items():
                if not filter_callback(k):
                    continue
                prefix.append(k)
                self._convert_mongo_2_sheet(
                    v, interval, prefix, result, filter_callback)
                prefix.pop()
        elif isinstance(document, list):
            # 当list里面放的不是单个的str元素，而是dict又是包含了字典的话就有问题...
            # result[interval.join(prefix)] = interval.join(document)
            # 那么尝试对于list来说，也给他增加一个prefix
            for d in document:
                # 对于list类型来说，不需要上面的prefix
                self._convert_mongo_2_sheet(
                    d, interval, prefix, result, filter_callback)
        else:
            result[interval.join(prefix)] = document
        return result

    def filter_sheet(self, key):
        return True

    def escape_double_quot(self, result):
        return result.replace('"', '""')

if __name__ == '__main__':
    bast_etl().parse_cmd()
