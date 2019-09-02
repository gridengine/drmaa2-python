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

import random
from .utils import generate_random_string
from .utils import needs_uge
from drmaa2 import ReservationSession


@needs_uge
def test_list_session_names():
    session_names = ReservationSession.list_session_names()
    assert (type(session_names) == type([]))
    print('\nThere are %s existing sessions: %s' % (len(session_names), session_names))


def test_new_session():
    session_name = generate_random_string()
    existing_session_names = ReservationSession.list_session_names()
    rs = ReservationSession(session_name)
    session_names = ReservationSession.list_session_names()
    assert (len(session_names) == len(existing_session_names) + 1)
    print('\nCreated new session: %s' % (session_name))


def test_existing_session():
    session_name = generate_random_string()
    existing_session_names = ReservationSession.list_session_names()
    rs = ReservationSession(session_name, destroy_on_exit=False)
    session_names = ReservationSession.list_session_names()
    assert (len(session_names) == len(existing_session_names) + 1)
    print('\nCreated new session: %s' % (session_name))
    del rs
    rs = ReservationSession(session_name)
    session_names2 = ReservationSession.list_session_names()
    assert (len(session_names) == len(session_names2))
    print('Opened existing session: %s' % (session_name))
    del rs
    session_names3 = ReservationSession.list_session_names()
    assert (len(session_names3) == len(existing_session_names))
    print('Closed session: %s' % (session_name))


def test_destroy_session():
    session_names = ReservationSession.list_session_names()
    print('\nExisting session names: %s' % session_names)
    for name in session_names:
        print('Destroying session: %s' % name)
        ReservationSession.destroy_by_name(name)
    session_names = ReservationSession.list_session_names()
    print('Remaining session names: %s' % session_names)
    assert (len(session_names) == 0)


def test_request_reservation():
    rs = ReservationSession('rs-01')
    r_name = 'reservation-%s' % int(random.uniform(0, 1000))
    r = rs.request_reservation({'reservation_name': r_name, 'duration': 100})
    print('\nRequested reservation: %s' % r)
    ri = r.get_info()
    assert (ri.reservation_name == r_name)
    print('Got reservation info: %s' % ri)


def test_get_reservations():
    rs = ReservationSession('rs-01')
    r_name = 'reservation-%s' % int(random.uniform(0, 1000))
    r = rs.request_reservation({'reservation_name': r_name, 'duration': 100})
    print('\nRequested reservation: %s' % r)
    r_list = rs.get_reservations()
    print('Got reservations: %s' % r_list)
    assert (len(r_list) >= 1)
    r_found = False
    for r2 in r_list:
        if r2.id == r.id:
            r_found = True
            break
    assert (r_found)
    r.terminate()


def test_get_reservation():
    rs = ReservationSession('rs-01')
    r_name = 'reservation-%s' % int(random.uniform(0, 1000))
    r = rs.request_reservation({'reservation_name': r_name, 'duration': 100})
    print(r)
    r2 = rs.get_reservation(r.id)
    assert (r2.id == r.id)
    print('Got reservation: %s' % r)
