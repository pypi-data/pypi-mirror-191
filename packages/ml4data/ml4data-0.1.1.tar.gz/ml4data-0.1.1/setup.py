#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='ml4data',
      version='0.1.0',
      description='ML4Data client library',
      author='ML4Data Team',
      author_email='info@ml4data.com',
      url='https://ml4data.com/',
      packages=find_packages(),
      install_requires=[
        'requests>=2.22.0',
        'Pillow>=6.2.1'
      ]
     )
