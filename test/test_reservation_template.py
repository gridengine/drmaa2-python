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

import datetime
from .utils import generate_random_string
from .utils import generate_random_int
from drmaa2 import ReservationSession
from drmaa2 import ReservationTemplate
from drmaa2 import Os
from drmaa2 import Cpu
from drmaa2.drmaa2_constants import POSIX_EPOCH


def test_reservation_template_from_reservation():
    rs = ReservationSession('rs-01')
    reservation_name = 'r.%s' % generate_random_string()
    r = rs.request_reservation({'reservation_name': reservation_name, 'duration': 100})
    rt = r.get_template()
    assert (rt.reservation_name == reservation_name)
    print('\nReservation template from reservation: %s' % (rt))


def test_get_implementation_specific_keys():
    keys = ReservationTemplate.get_implementation_specific_keys()
    assert (len(keys) > 0)
    print('\nReservation template implementation specific keys: %s' % (keys))


def test_reservation_name_attr():
    rt = ReservationTemplate()
    reservation_name = generate_random_string()
    rt.reservation_name = reservation_name
    assert (rt.reservation_name == reservation_name)
    print('\nReservation template with reservation_name: %s' % (reservation_name))


def test_start_time_attr():
    start_time = datetime.datetime.now()
    rt = ReservationTemplate()
    rt.start_time = start_time
    assert (int((rt.start_time - POSIX_EPOCH).total_seconds()) == int((start_time - POSIX_EPOCH).total_seconds()))
    print('\nReservation template object with start_time: %s' % (start_time))


def test_end_time_attr():
    end_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    rt = ReservationTemplate()
    rt.end_time = end_time
    assert (int((rt.end_time - POSIX_EPOCH).total_seconds()) == int((end_time - POSIX_EPOCH).total_seconds()))
    print('\nReservation template object with end_time: %s' % (end_time))


def test_duration_attr():
    rt = ReservationTemplate()
    duration = generate_random_int(lower_bound=1, upper_bound=86400)
    rt.duration = duration
    assert (rt.duration == duration)
    print('\nReservation template with duration: %s' % (duration))


def test_min_slots_attr():
    rt = ReservationTemplate()
    min_slots = generate_random_int(lower_bound=1, upper_bound=1024)
    rt.min_slots = min_slots
    assert (rt.min_slots == min_slots)
    print('\nReservation template with min_slots: %s' % (min_slots))


def test_max_slots_attr():
    rt = ReservationTemplate()
    max_slots = generate_random_int(lower_bound=1, upper_bound=1024)
    rt.max_slots = max_slots
    assert (rt.max_slots == max_slots)
    print('\nReservation template with max_slots: %s' % (max_slots))


def test_job_category_attr():
    rt = ReservationTemplate()
    job_category = generate_random_string()
    rt.job_category = job_category
    assert (rt.job_category == job_category)
    print('\nReservation template with job_category: %s' % (job_category))


def test_users_acl_attr():
    users_acl = []
    n_users_acl = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_users_acl):
        users_acl.append(generate_random_string())
    rt = ReservationTemplate()
    rt.users_acl = users_acl
    assert (rt.users_acl == users_acl)
    print('\nreservation template object with %s users_acl: %s' % (len(users_acl), users_acl))


def test_candidate_machines_attr():
    candidate_machines = []
    n_candidate_machines = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_candidate_machines):
        candidate_machines.append(generate_random_string())
    rt = ReservationTemplate()
    rt.candidate_machines = candidate_machines
    assert (rt.candidate_machines == candidate_machines)
    print(
        '\nreservation template object with %s candidate_machines: %s' % (len(candidate_machines), candidate_machines))


def test_min_phys_memory_attr():
    rt = ReservationTemplate()
    min_phys_memory = generate_random_int(lower_bound=1, upper_bound=86400)
    rt.min_phys_memory = min_phys_memory
    assert (rt.min_phys_memory == min_phys_memory)
    print('\nReservation template with min_phys_memory: %s' % (min_phys_memory))


def test_machine_os_attr():
    rt = ReservationTemplate()
    machine_os = generate_random_int(lower_bound=0, upper_bound=11)
    rt.machine_os = machine_os
    assert (rt.machine_os == Os(machine_os).name)
    print('\nReservation template with machine_os: %s' % (machine_os))


def test_machine_arch_attr():
    machine_arch = generate_random_int(lower_bound=0, upper_bound=16)
    rt = ReservationTemplate()
    rt.machine_arch = machine_arch
    assert (rt.machine_arch == Cpu(machine_arch).name)
    print('\nReservation template object with machine_arch: %s' % (machine_arch))


def test_implementation_specific_attr():
    implementation_specific = {}
    keys = ReservationTemplate.get_implementation_specific_keys()
    for k in keys:
        v = generate_random_string()
        implementation_specific[k] = v
    rt = ReservationTemplate()
    rt.implementation_specific = implementation_specific
    assert (rt.implementation_specific == implementation_specific)
    print('\nReservation template object with implementation_specific: %s' % (implementation_specific))
