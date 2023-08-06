#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='sophontool',
    version='0.0.7',
    author='yifei.gao, wangyang.zuo',
    author_email='yifei.gao@sophgo.com, wangyang.zuo@sophon.com',
    description='tools for sophon',
    packages=['stool'],
    package_data={'stool':['*.so']},
    include_package_data = True,
    entry_points={ 'console_scripts': ['stool = stool.main:main'] },
    scripts=['stool/main.py'],
    install_requires=["requests","tqdm","pycrypto"]
)
# pipzwyqwerty123

