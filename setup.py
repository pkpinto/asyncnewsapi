#!/usr/bin/env python

from setuptools import setup, find_namespace_packages


INSTALL_REQUIRES = [
    'aiohttp>=3.5,<4', 'async_timeout', 'yarl'
]
TEST_REQUIRES = [
    # testing and coverage
    'pytest<5.3', 'pytest-cov',
]

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='asyncnewsapi',
    version='0.2.1',
    description='AsyncIO Python wrapper to News API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    url='https://github.com/pkpinto/asyncnewsapi',
    author='Paulo Kauscher Pinto',
    author_email='paulo.kauscher.pinto@icloud.com',
    license='Apache License 2.0',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'test': TEST_REQUIRES + INSTALL_REQUIRES,
    },
)
