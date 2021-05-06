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

from .utils import generate_random_string
from drmaa2 import JobSession
from drmaa2 import JobState


def test_terminate():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['10'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 3, 2)
    ja.terminate()
    j_list = ja.job_list
    failed_jobs = []
    for j in j_list:
        s, ss = j.get_state()
        if s == JobState.FAILED:
            failed_jobs.append(j)
    assert (len(failed_jobs) > 0)
    print('\nTerminate job array: %s' % (ja))


def test_suspend_and_resume():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 3, 2)
    j_list = ja.job_list
    js.wait_any_started(j_list)
    ja.suspend()
    suspended_jobs = []
    for j in j_list:
        s, ss = j.get_state()
        if s == JobState.SUSPENDED:
            suspended_jobs.append(j)
    assert (len(suspended_jobs) > 0)
    print('\nSuspend job array: %s' % (ja))
    ja.resume()
    for j in suspended_jobs:
        s, ss = j.get_state()
        assert (s != JobState.SUSPENDED)
    print('Resume job array: %s' % (ja))


def test_hold_and_release():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 3, 2)
    ja.hold()
    held_jobs = []
    j_list = ja.job_list
    for j in j_list:
        s, ss = j.get_state()
        if s.name.endswith('HELD'):
            held_jobs.append(j)
    assert (len(held_jobs) > 0)
    print('\nHold job array: %s' % (ja))
    ja.release()
    for j in held_jobs:
        s, ss = j.get_state()
        assert (not s.name.endswith('HELD'))
    print('Release job array: %s' % (ja))


def test_get_template():
    session_name = generate_random_string()
    js = JobSession(session_name)
    job_name = 'drmaa2python-%s' % generate_random_string()
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'job_name': job_name, 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 3, 2)
    jt = ja.get_template()
    assert (jt.job_name == job_name)
    print('\nGet template: %s' % (jt))
