#!/usr/bin/env python

import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='asyncnewsapi',
    version='0.1',
    description='AsyncIO Python wrapper to News API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    url='https://github.com/pkpinto/asyncnewsapi',
    author='Paulo Kauscher Pinto',
    author_email='paulo.kauscher.pinto@icloud.com',
    license='Apache License 2.0',
    packages=['asyncnewsapi'],
    install_requires=['aiohttp>=3.5,<4', 'pytest<5.3'],
)
