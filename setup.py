# -*- coding: utf-8 -*-
import setuptools


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setuptools.setup(
    name='Octagon',
    version='0.2',
    description='How can I find an octagon? How, Elmo? How?',
    long_description=readfile('README.md'),
    long_description_content_type="text/markdown",
    author='Cloud11665',
    author_email='Cloud11665@gmail.com',
    url='https://github.com/Cloud11665/octagon',
    packages=setuptools.find_packages(),
    license=readfile('LICENSE'),
    entry_points={
        'console_scripts': ['octagon = code.__init__']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
