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

import drmaa2


def test_get_drms_version():
    v = drmaa2.get_drms_version()
    assert (v.major != '' and v.minor != '')
    print('\nGot DRMS version: %s' % (v))


def test_get_drmaa_version():
    v = drmaa2.get_drmaa_version()
    assert (v.major != '' and v.minor != '')
    print('\nGot DRMAA version: %s' % (v))


def test_get_drms_name():
    n = drmaa2.get_drms_name()
    assert (n != '')
    print('\nGot DRMS name: %s' % (n))


def test_get_drmaa_name():
    n = drmaa2.get_drmaa_name()
    assert (n != '')
    print('\nGot DRMAA name: %s' % (n))


def test_drmaa_supports():
    print('\nVerifying support for %s capabilities' % (len(drmaa2.Capability)))
    supported = []
    for c in drmaa2.Capability:
        s = drmaa2.drmaa_supports(c)
        if s:
            supported.append(s)
        print('Support for %s: %s' % (c, s))
    assert (len(supported) > 0)
    print('DRMAA2 supports %s out of %s capabilities' % (len(supported), len(drmaa2.Capability)))


def test_get_job_session_names():
    sessions = drmaa2.get_job_session_names()
    assert (type(sessions) == type([]))
    print('\nGot %s job sessions: %s' % (len(sessions), sessions))


def test_get_reservation_session_names():
    sessions = drmaa2.get_reservation_session_names()
    assert (type(sessions) == type([]))
    print('\nGot %s reservation sessions: %s' % (len(sessions), sessions))
