#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : 玛卡玛卡啊
# @Time     : 2022/11/28 20:58
# @desc     : 作者的所有代码均属于学习使用,不可商用或用在非法用途上。
# 打包成模块压缩包
import setuptools
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="fucker-easy",  # 模块名称
    version="0.1.1",  # 当前版本
    author="songtao",  # 作者
    author_email="",  # 作者邮箱
    description="一个非常NB的包",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://gitee.com/deathoffish/lazy-toolsr",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'requests',
    ],
    python_requires='>=3',
)
