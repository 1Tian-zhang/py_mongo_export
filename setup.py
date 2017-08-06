# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2017-08-03 12:35:51

from setuptools import setup

setup(
    name="py_mongo_export",
    version="1.0",
    author="yiTian.zhang",
    author_email="hhczy1003@163.com",
    packages=["py_mongo_export"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["py_mongo_export = easyspider.crawler.easyspider.core.cmdline:execute"]
    }
)
