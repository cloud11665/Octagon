# -*- coding: utf-8 -*-
import setuptools


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setuptools.setup(
    name='Octagon',
    version='1.0.6',
    description='How can I find an octagon? How, Elmo? How?',
    long_description=readfile('README.md'),
    long_description_content_type="text/markdown",
    author='Cloud11665',
    author_email='Cloud11665@gmail.com',
    url='https://github.com/Cloud11665/octagon',
    packages=setuptools.find_packages(),
    license='gpl-3.0',
    entry_points={
        'console_scripts': ['octagon = Octagon.__init__:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
