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

import os
import random
from drmaa2 import MonitoringSession
from drmaa2 import JobSession
from drmaa2 import ReservationSession
from drmaa2 import JobInfo
from .utils import needs_uge


@needs_uge
def test_get_all_queues():
    q_name_list = os.popen('qconf -sql').read().split()
    print('\nGot queue list: %s' % q_name_list)
    ms = MonitoringSession('ms-01')
    qi_list = ms.get_all_queues(q_name_list)
    assert (len(qi_list) == len(q_name_list))
    for qi in qi_list:
        q_name = qi.name
        print('Checking queue: %s' % (qi.to_dict()))
        assert (q_name in q_name_list)


def test_get_all_machines():
    h_name_list = os.popen('qconf -sel').read().split()
    print('\nGot host list: %s' % h_name_list)
    ms = MonitoringSession('ms-01')
    mi_list = ms.get_all_machines(h_name_list)
    assert (len(mi_list) == len(h_name_list))
    for mi in mi_list:
        h_name = mi.name
        print('Checking machine: %s' % (mi.to_dict()))
        assert (h_name in h_name_list)


def test_get_all_jobs():
    js = JobSession('js-01')
    j_name = 'drmaa2python-%s' % int(random.uniform(0, 1000))
    d = {'remote_command': '/bin/sleep', 'args': ['10'], 'job_name': j_name, 'output_path': '/dev/null', 'join_files': True}
    j = js.run_job(d)
    print('\nSubmitted job: %s' % j)
    ji = j.get_info()
    j.wait_started()
    ms = MonitoringSession('ms-01')
    print('Opened monitoring session: %s' % ms.name)
    ji2 = JobInfo({'job_id': ji.job_id})
    print('Retrieving jobs matching job info %s' % ji2)
    j_list = ms.get_all_jobs(ji2)
    print('Got all jobs: %s' % j_list)
    assert (len(j_list) >= 1)


def test_get_all_reservatios():
    rs = ReservationSession('rs-01')
    r_name = 'drmaa2python-%s' % int(random.uniform(0, 1000))
    d = {'reservation_name': r_name, 'duration': 100}
    r = rs.request_reservation(d)
    print('\nCreated reservation: %s' % r)
    ri = r.get_info()
    # At the moment one cannot have both reservation and monitoring 
    # sessions opened at the same time
    rs.close()

    ms = MonitoringSession('ms-01')
    print('Retrieving reservations matching reservation info %s' % ri)
    r_list = ms.get_all_reservations(ri)
    print('Got all reservations: %s' % r_list)
    assert (len(r_list) == 1)
