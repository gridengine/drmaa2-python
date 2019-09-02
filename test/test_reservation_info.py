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

import datetime
from .utils import generate_random_string
from .utils import generate_random_int
from drmaa2 import ReservationSession
from drmaa2 import ReservationInfo
from drmaa2.drmaa2_constants import POSIX_EPOCH


def test_reservation_info_from_reservation():
    rs = ReservationSession('rs-01')
    reservation_name = 'r.%s' % generate_random_string()
    r = rs.request_reservation({'reservation_name': reservation_name, 'duration': 100})
    ri = r.get_info()
    assert (ri.reservation_name == reservation_name)
    print('\nReservation info from reservation: %s' % (ri))


def test_get_implementation_specific_keys():
    keys = ReservationInfo.get_implementation_specific_keys()
    assert (len(keys) > 0)
    print('\nReservation info implementation specific keys: %s' % (keys))


def test_reservation_id_attr():
    ri = ReservationInfo()
    reservation_id = generate_random_string()
    ri.reservation_id = reservation_id
    assert (ri.reservation_id == reservation_id)
    print('\nReservation info with reservation_id: %s' % (reservation_id))


def test_reservation_name_attr():
    ri = ReservationInfo()
    reservation_name = generate_random_string()
    ri.reservation_name = reservation_name
    assert (ri.reservation_name == reservation_name)
    print('\nReservation info with reservation_name: %s' % (reservation_name))


def test_reserved_start_time_attr():
    reserved_start_time = datetime.datetime.now()
    ri = ReservationInfo()
    ri.reserved_start_time = reserved_start_time
    assert (int((ri.reserved_start_time - POSIX_EPOCH).total_seconds()) == int(
        (reserved_start_time - POSIX_EPOCH).total_seconds()))
    print('\nReservation info object with reserved_start_time: %s' % (reserved_start_time))


def test_reserved_end_time_attr():
    reserved_end_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    ri = ReservationInfo()
    ri.reserved_end_time = reserved_end_time
    assert (int((ri.reserved_end_time - POSIX_EPOCH).total_seconds()) == int(
        (reserved_end_time - POSIX_EPOCH).total_seconds()))
    print('\nReservation info object with reserved_end_time: %s' % (reserved_end_time))


def test_users_acl_attr():
    users_acl = []
    n_users_acl = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_users_acl):
        users_acl.append(generate_random_string())
    ri = ReservationInfo()
    ri.users_acl = users_acl
    assert (ri.users_acl == users_acl)
    print('\nreservation info object with %s users_acl: %s' % (len(users_acl), users_acl))


def test_reserved_slots_attr():
    ri = ReservationInfo()
    reserved_slots = generate_random_int(lower_bound=1, upper_bound=1024)
    ri.reserved_slots = reserved_slots
    assert (ri.reserved_slots == reserved_slots)
    print('\nReservation info with reserved_slots: %s' % (reserved_slots))


def test_reserved_machines_attr():
    reserved_machines = []
    n_reserved_machines = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_reserved_machines):
        reserved_machines.append(generate_random_string())
    ri = ReservationInfo()
    ri.reserved_machines = reserved_machines
    assert (ri.reserved_machines == reserved_machines)
    print('\nreservation info object with %s reserved_machines: %s' % (len(reserved_machines), reserved_machines))


def test_implementation_specific_attr():
    implementation_specific = {}
    keys = ReservationInfo.get_implementation_specific_keys()
    for k in keys:
        v = generate_random_string()
        implementation_specific[k] = v
    ri = ReservationInfo()
    ri.implementation_specific = implementation_specific
    assert (ri.implementation_specific == implementation_specific)
    print('\nReservation info object with implementation_specific: %s' % (implementation_specific))
