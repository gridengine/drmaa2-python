#!/usr/bin/env python
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

from drmaa2 import Version


def test_get_drms_version():
    v = Version.get_drms_version()
    assert (v.major != '' and v.minor != '')
    print('\nGot DRMS version: %s' % (v))


def test_get_drmaa_version():
    v = Version.get_drmaa_version()
    assert (v.major != '' and v.minor != '')
    print('\nGot DRMAA version: %s' % (v))


def test_to_dict():
    v = Version.get_drmaa_version()
    d = v.to_dict()
    assert (v.major == d['major'])
    assert (v.minor == d['minor'])
    print('\nVersion object conversion to dictionary: %s' % (d))


def test_get_implementation_specific_keys():
    keys = Version.get_implementation_specific_keys()
    assert (keys is not None)
    print('\nVersion object has %s impl specific keys %s.' % (len(keys), keys))


def test_get_implementation_specific_attrs():
    attrs = Version.get_implementation_specific_attrs()
    assert (attrs is not None)
    print('\nVersion object has %s impl specific attrs %s.' % (len(attrs), attrs))
