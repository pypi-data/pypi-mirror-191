#!usr/bin/python3
# -*- coding: utf-8 -*-


from setuptools import setup

from sbo_create.__metadata__ import (
    __prog__,
    __version__,
    __author__,
    __email__,
    __website__,
)

setup(
    name=__prog__,
    packages=['sbo_create'],
    scripts=['bin/sbo-create'],
    version=__version__,
    description='SBo tool for creating SlackBuilds.',
    long_description=open('README.rst').read(),
    keywords=['sbo', 'templates', 'slackbuild'],
    author=__author__,
    author_email=__email__,
    url=__website__,
    package_data={'': ['LICENSE', 'README.rst', 'ChangeLog.txt']},
    install_requires=[
        'pythondialog>=3.5.3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        ],
    python_requires='>=3.7'
)
