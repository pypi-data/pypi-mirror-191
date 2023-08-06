#!/usr/bin/env python
# coding: utf-8

#############################################
# File Name: setup.py
# Author: whzcorcd
# Mail: whzcorcd@gmail.com
# Created Time:  2020-06-08
#############################################

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="multi-wechat-webhook",
    version='0.0.2',
    author='badx',
    author_email='badx16@gmail.com',
    url='https://github.com/corcd/sentry-wechat',
    description='A sentry extension which share information to Wechat Work',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='sentry multi wechat',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'multi_wechat_webhook = multi_wechat_webhook.plugin:WechatPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: MIT License",
    ]
)
