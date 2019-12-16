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
import socket
from .utils import generate_random_string
from .utils import generate_random_int
from drmaa2 import JobSession
from drmaa2 import JobInfo
from drmaa2 import JobState
from drmaa2.drmaa2_constants import POSIX_EPOCH


def test_job_info_from_job():
    session_name = generate_random_string()
    js = JobSession(session_name)
    jn = 'drmaa2python-%s' % generate_random_string()
    d = {'remote_command': '/bin/sleep', 'args': ['10'], 'job_name': jn}
    j = js.run_job(d)
    ji = j.get_info()
    assert (ji.job_name == jn)
    print('\nJob info from job: %s' % (ji))


def test_get_implementation_specific_keys():
    keys = JobInfo.get_implementation_specific_keys()
    assert (len(keys) > 0)
    print('\nJob info implementation specific keys: %s' % (keys))


def test_job_id_attr():
    ji = JobInfo()
    job_id = generate_random_string()
    ji.job_id = job_id
    assert (ji.job_id == job_id)
    print('\nJob info with job_id: %s' % (job_id))


def test_job_name_attr():
    ji = JobInfo()
    job_name = generate_random_string()
    ji.job_name = job_name
    assert (ji.job_name == job_name)
    print('\nJob info with job_name: %s' % (job_name))


def test_exit_status_attr():
    ji = JobInfo()
    exit_status = generate_random_int(lower_bound=0, upper_bound=255)
    ji.exit_status = exit_status
    assert (ji.exit_status == exit_status)
    print('\nJob info with exit_status: %s' % (exit_status))


def test_terminating_signal_attr():
    ji = JobInfo()
    terminating_signal = generate_random_string()
    ji.terminating_signal = terminating_signal
    assert (ji.terminating_signal == terminating_signal)
    print('\nJob info with terminating_signal: %s' % (terminating_signal))


def test_annotation_attr():
    ji = JobInfo()
    annotation = generate_random_string()
    ji.annotation = annotation
    assert (ji.annotation == annotation)
    print('\nJob info with annotation: %s' % (annotation))


def test_job_state_attr():
    ji = JobInfo()
    job_state = JobState(generate_random_int(lower_bound=0, upper_bound=9))
    ji.job_state = job_state
    assert (ji.job_state == job_state.name)
    print('\nJob info with job_state: %s' % (job_state))


def test_job_sub_state_attr():
    ji = JobInfo()
    job_sub_state = generate_random_string()
    ji.job_sub_state = job_sub_state
    assert (ji.job_sub_state == job_sub_state)
    print('\nJob info with job_sub_state: %s' % (job_sub_state))


def test_allocated_machines_attr():
    allocated_machines = []
    n_allocated_machines = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_allocated_machines):
        allocated_machines.append(generate_random_string())
    ji = JobInfo()
    ji.allocated_machines = allocated_machines
    assert (ji.allocated_machines == allocated_machines)
    print('\nJob info object with %s allocated_machines: %s' % (len(allocated_machines), allocated_machines))


def test_submission_machine_attr():
    ji = JobInfo()
    submission_machine = socket.gethostname()
    ji.submission_machine = submission_machine
    assert (ji.submission_machine == submission_machine)
    print('\nJob info with submission_machine: %s' % (submission_machine))


def test_job_owner_attr():
    ji = JobInfo()
    job_owner = generate_random_string()
    ji.job_owner = job_owner
    assert (ji.job_owner == job_owner)
    print('\nJob info with job_owner: %s' % (job_owner))


def test_slots_attr():
    ji = JobInfo()
    slots = generate_random_int(lower_bound=0, upper_bound=1024)
    ji.slots = slots
    assert (ji.slots == slots)
    print('\nJob info with slots: %s' % (slots))


def test_queue_name_attr():
    ji = JobInfo()
    queue_name = generate_random_string()
    ji.queue_name = queue_name
    assert (ji.queue_name == queue_name)
    print('\nJob info with queue_name: %s' % (queue_name))


def test_wallclock_time_attr():
    ji = JobInfo()
    wallclock_time = datetime.datetime.fromtimestamp(generate_random_int(lower_bound=0, upper_bound=12386400))
    ji.wallclock_time = wallclock_time
    assert (ji.wallclock_time == wallclock_time)
    print('\nJob info with wallclock_time: %s' % (wallclock_time))


def test_cpu_time_attr():
    ji = JobInfo()
    cpu_time = generate_random_int(lower_bound=0, upper_bound=86400)
    ji.cpu_time = cpu_time
    assert (ji.cpu_time == cpu_time)
    print('\nJob info with cpu_time: %s' % (cpu_time))


def test_submission_time_attr():
    submission_time = datetime.datetime.now()
    ji = JobInfo()
    ji.submission_time = submission_time
    assert (int((ji.submission_time - POSIX_EPOCH).total_seconds()) == int(
        (submission_time - POSIX_EPOCH).total_seconds()))
    print('\nJob info object with submission_time: %s' % (submission_time))


def test_dispatch_time_attr():
    dispatch_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    ji = JobInfo()
    ji.dispatch_time = dispatch_time
    assert (int((ji.dispatch_time - POSIX_EPOCH).total_seconds()) == int((dispatch_time - POSIX_EPOCH).total_seconds()))
    print('\nJob info object with dispatch_time: %s' % (dispatch_time))


def test_finish_time_attr():
    finish_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    ji = JobInfo()
    ji.finish_time = finish_time
    assert (int((ji.finish_time - POSIX_EPOCH).total_seconds()) == int((finish_time - POSIX_EPOCH).total_seconds()))
    print('\nJob info object with finish_time: %s' % (finish_time))


def test_implementation_specific_attr():
    implementation_specific = {}
    keys = JobInfo.get_implementation_specific_keys()
    for k in keys:
        v = generate_random_string()
        implementation_specific[k] = v
    ji = JobInfo()
    ji.implementation_specific = implementation_specific
    assert (ji.implementation_specific == implementation_specific)
    print('\nJob info object with implementation_specific: %s' % (implementation_specific))
