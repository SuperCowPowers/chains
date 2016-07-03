import os
import sys

from setuptools import setup

# Project Information 
dist_name = 'chains'
package_name = 'chains'
description = 'Exploratory Python Chained Generator Project'
with open('README.rst') as f:
    long_description = f.read()

scripts = ['scripts/netwatch', 'scripts/urlwatch']
packages = ['chains', 'chains.links', 'chains.sinks', 'chains.sources', 'chains.utils']

requirements = ['pypcap==1.1.4.1', 'dpkt', 'netifaces']
test_requirements = []

# Pull in the version from the package
package = __import__(package_name)
version = package.__version__

setup(
      name=dist_name,
      version=package.__version__,
      author=package.__author__,
      author_email=package.__author_email__,
      url=package.__url__,
      description=description,
      long_description=long_description,
      scripts=scripts,
      packages=packages,
      install_requires=requirements,
      license='MIT',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      tests_require=test_requirements
)
