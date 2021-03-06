#!/usr/bin/env python

from setuptools import setup


setup(name='vcert',
      version='0.5.1',
      url="https://github.com/Venafi/vcert-python",
      packages=['vcert'],
      install_requires=['requests>=2.6.0', 'python-dateutil>=2.6.1', 'certvalidator',
                        'enum34', 'ipaddress', 'cryptography'],
      description='Python bindings for Venafi TPP/Venfi Cloud API.',
      author='Denis Subbotin',
      author_email='denis.subbotin@venafi.com',
      license='ASL',
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Operating System :: OS Independent',
          "License :: OSI Approved :: Apache Software License",
      ])

