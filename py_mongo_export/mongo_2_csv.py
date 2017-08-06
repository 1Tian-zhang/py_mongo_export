# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-07-19 09:08:33
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-08-05 23:20:11

import logging
from base_etl import base_etl

logger = logging.getLogger(__name__)


class mongo_2_csv(base_etl):

    def save_all_sheet_result(self, valid_sheet_result, args):
        csv_file, split_symbol = args.csv_file, args.split
        fields = set()
        for result in valid_sheet_result:
            for k in result.keys():
                fields.add(k)
        fields = list(fields)
        with open(csv_file, "w") as f:
            f.write("%s\n" % split_symbol.join(
                ['"%s"' % self.escape_double_quot(field) for field in fields]))
            for result in valid_sheet_result:
                f.write("%s\n" % split_symbol.join(
                    ['"%s"' % self.escape_double_quot(str(result.get(key, "None"))) for key in fields]))
        logger.info("all successed, write down csv file %s" % csv_file)


if __name__ == '__main__':
    mongo_2_csv().run()
