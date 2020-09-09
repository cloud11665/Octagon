# -*- coding: utf-8 -*-
import setuptools


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setuptools.setup(
    name='Octagon',
    version='0.2',
    description='',
    long_description=readfile('README.md'),
    author='Cloud11665',
    author_email='Cloud11665@gmail.com',
    url='https://github.com/Cloud11665/octagon',
    license=readfile('LICENSE'),
    entry_points={
        'console_scripts': [
            'octagon = code/__init__:main'
        ]
    }
)