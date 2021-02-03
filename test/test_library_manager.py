#!/usr/bin/env python
# ___INFO__MARK_BEGIN__
#######################################################################################
# Copyright 2008-2021 Univa Corporation (acquired and owned by Altair Engineering Inc.)
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#######################################################################################
# ___INFO__MARK_END__

from drmaa2 import LibraryManager
from drmaa2 import Capability


def test_get_drms_name():
    lm = LibraryManager.get_instance()
    n = lm.get_drms_name()
    assert (n != '')
    print('\nGot DRMS name: %s' % (n))


def test_get_drmaa_name():
    lm = LibraryManager.get_instance()
    n = lm.get_drmaa_name()
    assert (n != '')
    print('\nGot DRMAA name: %s' % (n))


def test_drmaa_supports():
    lm = LibraryManager.get_instance()
    print('\nVerifying support for %s capabilities' % (len(Capability)))
    supported = []
    for c in Capability:
        s = lm.drmaa_supports(c)
        if s:
            supported.append(s)
        print('Support for %s: %s' % (c, s))
    assert (len(supported) > 0)
    print('DRMAA2 supports %s out of %s capabilities' % (len(supported), len(Capability)))
