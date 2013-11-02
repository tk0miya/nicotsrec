# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='nicotsrec',
    version='0.1.0',
    description='nicovideo-live timeshift recorder',
    author='Takeshi Komiya',
    author_email='i.tkomiya at gmail.com',
    license='Apache License 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'pit',
    ],
    entry_points="""
       [console_scripts]
       nicotsrec = nicotsrec:main
    """
)
