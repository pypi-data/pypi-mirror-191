"""
***************************
--------description--------
Author: chenxu.tian 472159011@qq.com
Date: 2023-02-10 22:03:38
LastEditors: chenxu.tian 472159011@qq.com
LastEditTime: 2023-02-10 22:35:44
FilePath: /test_platform_helper/setup.py
Description: 

Copyright (c) 2023 by chenxu.tian 472159011@qq.com, All Rights Reserved. 

***************************
"""
from setuptools import setup, find_packages


setup(
    packages=find_packages(exclude=("tests", "tests.*", "node_modules"))
)
