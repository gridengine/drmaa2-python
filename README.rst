(c) Copyright 2008-2021 Univa Corporation (acquired and owned by Altair Engineering Inc.)
    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License.

    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

    See the License for the specific language governing permissions and
    limitations under the License.

UGE DRMAA v2 Python API
=======================

Prerequisites
-------------

UGE DRMAA2 requires recent versions of the following software:

1. UGE (8.6.8 or above)
2. Python (v2.7.5 or later in 2.7 series, or in any 3.x series)
3. Setuptools (0.9.8 or later; for egg installation)
4. Nose (1.3.7 or later; for testing)
5. Sphinx (1.1.3 or later; for generating documentation)
6. Standard development tools (make)
7. Python wheel module (0.32.3 or later; for generating wheel package)
8. enum34 module for IntEnum (remove enum module)

The software versions listed above were used for API development and
testing, on CentOS 7.2 (64-bit).

Build/Package
-------------

In the top level directory run:

.. code:: sh

     $ make clean
     $ make

This command should create installable egg and wheel packages, as well
as generate documentation and copy it into the ``dist`` directory.

Basic API Usage
---------------

For simple testing, without installing UGE DRMAA2 egg or wheel package,
do the following:

1) Setup SGE environment:

.. code:: sh

     $ source $SGE_ROOT/$SGE_CELL/common/settings.sh

2) Setup PYTHONPATH environment variable to point to the top level
   directory:

.. code:: sh

     $ export PYTHONPATH=<UGE_DRMAA2_PYTHON_ROOT>

This step is not needed if UGE DRMAA2 egg or wheel package is installed.

3) At this point you can import and use the drmaa2 module:

.. code:: sh

     $ python
     >>> import drmaa2
     >>> print(drmaa2.get_drmaa_name())
     Univa Grid Engine Drmaa V2

Note that there are a number of API usage examples located under the
``examples`` directory.

Running Test Suite
------------------

1) Setup SGE environment:

.. code:: sh

     $ source $SGE_ROOT/$SGE_CELL/common/settings.sh

2) In the top level directory run:

.. code:: sh

     $ make test
