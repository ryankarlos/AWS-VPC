#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Ryan Nazareth",
    author_email='ryankarlos@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Examples of AWS options for configuring VPC and allow network traffic to internet and other services",
    entry_points={
        'console_scripts': [
            'aws_vpc=aws_vpc.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='aws_vpc',
    name='aws_vpc',
    packages=find_packages(include=['aws_vpc', 'aws_vpc.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ryankarlos/aws_vpc',
    version='0.1.0',
    zip_safe=False,
)
