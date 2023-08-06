'''
Author: Vincent Young
Date: 2023-02-13 19:30:36
LastEditors: Vincent Young
LastEditTime: 2023-02-13 21:21:18
FilePath: /FreeDeepL/setup.py
Telegram: https://t.me/missuo

Copyright © 2023 by Vincent, All Rights Reserved. 
'''

from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="FreeDeepL",
    author="missuo",
    version="0.0.8",
    license='MIT',
    long_description= long_description,
    long_description_content_type="text/markdown",
    author_email="i@yyt.moe",
    description="Free DeepL Tranlaste",
    url='https://github.com/missuo/FreeDeepL',
    packages=find_packages(),
    include_package_data=False,
    platforms='any',
    zip_safe=False,

    install_requires=[
        'httpx'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)