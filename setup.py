# ___INFO__MARK_BEGIN__
########################################################################## 
# Copyright 2016-2019 Univa Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
########################################################################### 
# ___INFO__MARK_END__
from __future__ import with_statement, print_function
import sys

# Work around http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing
except ImportError:
    pass

try:
    from setuptools import setup

    extra = dict(include_package_data=True)
except ImportError:
    from distutils.core import setup

    extra = {}

import os

from drmaa2 import __version__

if sys.version_info <= (2, 7):
    error = "ERROR: UGE DRMAA2 API requires Python Version 2.7 or above...exiting."
    print(error, file=sys.stderr)
    sys.exit(1)

with open("README.rst") as f:
    long_description = f.read()

setup(name='uge-drmaa2',
      version=__version__,
      description='UGE DRMAA2 Python API',
      long_description=long_description,
      # long_description_content_type='text/markdown',
      author='Univa',
      author_email='info@univa.com',
      test_suite='test',
      url='https://www.univa.com',
      packages=['drmaa2'],
      install_requires=[],
      package_data={
      },
      license='Apache 2.0',
      platforms='Posix; MacOS X',
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
      **extra
      )
