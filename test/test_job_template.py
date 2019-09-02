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
from drmaa2 import JobTemplate
from drmaa2 import Bool
from drmaa2 import Os
from drmaa2 import Cpu
from drmaa2 import Drmaa2Exception
from drmaa2.drmaa2_constants import POSIX_EPOCH


def test_remote_command_attr():
    remote_command = generate_random_string()
    jt = JobTemplate()
    jt.remote_command = remote_command
    assert (jt.remote_command == remote_command)
    print('\nJob template object with remote_command: %s' % (remote_command))


def test_args_attr():
    args = []
    n_args = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_args):
        args.append(generate_random_string())
    jt = JobTemplate()
    jt.args = args
    assert (jt.args == args)
    print('\nJob template object with %s args: %s' % (len(args), args))


def test_submit_as_hold_attr():
    submit_as_hold = generate_random_int(lower_bound=0, upper_bound=1)
    jt = JobTemplate()
    jt.submit_as_hold = submit_as_hold
    assert (jt.submit_as_hold == Bool(submit_as_hold).name)
    print('\nJob template object with submit_as_hold: %s' % (submit_as_hold))


def test_rerunnable_attr():
    rerunnable = generate_random_int(lower_bound=0, upper_bound=1)
    jt = JobTemplate()
    jt.rerunnable = rerunnable
    assert (jt.rerunnable == Bool(rerunnable).name)
    print('\nJob template object with rerunnable: %s' % (rerunnable))


def test_job_environment_attr():
    job_environment = {}
    n_args = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_args):
        name = generate_random_string().upper()
        value = generate_random_string()
        job_environment[name] = value
    jt = JobTemplate()
    jt.job_environment = job_environment
    assert (jt.job_environment == job_environment)
    print('\nJob template object with job_environment: %s' % (job_environment))


def test_working_directory_attr():
    working_directory = generate_random_string()
    jt = JobTemplate()
    jt.working_directory = working_directory
    assert (jt.working_directory == working_directory)
    print('\nJob template object with working_directory: %s' % (working_directory))


def test_job_category_attr():
    job_category = generate_random_string()
    jt = JobTemplate()
    jt.job_category = job_category
    assert (jt.job_category == job_category)
    print('\nJob template object with job_category: %s' % (job_category))


def test_email_attr():
    email = []
    n_email = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_email):
        email.append(generate_random_string())
    jt = JobTemplate()
    jt.email = email
    assert (jt.email == email)
    print('\nJob template object with %s emails: %s' % (len(email), email))


def test_email_on_started_attr():
    email_on_started = generate_random_int(lower_bound=0, upper_bound=1)
    jt = JobTemplate()
    jt.email_on_started = email_on_started
    assert (jt.email_on_started == Bool(email_on_started).name)
    print('\nJob template object with email_on_started: %s' % (email_on_started))


def test_email_on_terminated_attr():
    email_on_terminated = generate_random_int(lower_bound=0, upper_bound=1)
    jt = JobTemplate()
    jt.email_on_terminated = email_on_terminated
    assert (jt.email_on_terminated == Bool(email_on_terminated).name)
    print('\nJob template object with email_on_terminated: %s' % (email_on_terminated))


def test_job_name_attr():
    job_name = generate_random_string()
    jt = JobTemplate()
    jt.job_name = job_name
    assert (jt.job_name == job_name)
    print('\nJob template object with job_name: %s' % (job_name))


def test_input_path_attr():
    input_path = generate_random_string()
    jt = JobTemplate()
    jt.input_path = input_path
    assert (jt.input_path == input_path)
    print('\nJob template object with input_path: %s' % (input_path))


def test_output_path_attr():
    output_path = generate_random_string()
    jt = JobTemplate()
    jt.output_path = output_path
    assert (jt.output_path == output_path)
    print('\nJob template object with output_path: %s' % (output_path))


def test_error_path_attr():
    error_path = generate_random_string()
    jt = JobTemplate()
    jt.error_path = error_path
    assert (jt.error_path == error_path)
    print('\nJob template object with error_path: %s' % (error_path))


def test_join_files_attr():
    join_files = generate_random_int(lower_bound=0, upper_bound=1)
    jt = JobTemplate()
    jt.join_files = join_files
    assert (jt.join_files == Bool(join_files).name)
    print('\nJob template object with join_files: %s' % (join_files))


def test_reservation_id_attr():
    reservation_id = generate_random_string()
    jt = JobTemplate()
    jt.reservation_id = reservation_id
    assert (jt.reservation_id == reservation_id)
    print('\nJob template object with reservation_id: %s' % (reservation_id))


def test_queue_name_attr():
    queue_name = generate_random_string()
    jt = JobTemplate()
    jt.queue_name = queue_name
    assert (jt.queue_name == queue_name)
    print('\nJob template object with queue_name: %s' % (queue_name))


def test_min_slots_attr():
    min_slots = generate_random_int(lower_bound=0, upper_bound=100)
    jt = JobTemplate()
    jt.min_slots = min_slots
    assert (jt.min_slots == min_slots)
    print('\nJob template object with min_slots: %s' % (min_slots))


def test_max_slots_attr():
    max_slots = generate_random_int(lower_bound=0, upper_bound=100)
    jt = JobTemplate()
    jt.max_slots = max_slots
    assert (jt.max_slots == max_slots)
    print('\nJob template object with max_slots: %s' % (max_slots))


def test_priority_attr():
    priority = generate_random_int(lower_bound=0, upper_bound=1000)
    jt = JobTemplate()
    jt.priority = priority
    assert (jt.priority == priority)
    print('\nJob template object with priority: %s' % (priority))


def test_candidate_machines_attr():
    candidate_machines = []
    n_candidate_machines = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_candidate_machines):
        candidate_machines.append(generate_random_string())
    jt = JobTemplate()
    jt.candidate_machines = candidate_machines
    assert (jt.candidate_machines == candidate_machines)
    print('\nJob template object with %s candidate_machines: %s' % (len(candidate_machines), candidate_machines))


def test_min_phys_memory_attr():
    min_phys_memory = generate_random_int(lower_bound=0, upper_bound=1000)
    jt = JobTemplate()
    jt.min_phys_memory = min_phys_memory
    assert (jt.min_phys_memory == min_phys_memory)
    print('\nJob template object with min_phys_memory: %s' % (min_phys_memory))


def test_machine_os_attr():
    machine_os = generate_random_int(lower_bound=0, upper_bound=11)
    jt = JobTemplate()
    jt.machine_os = machine_os
    assert (jt.machine_os == Os(machine_os).name)
    print('\nJob template object with machine_os: %s' % (machine_os))


def test_machine_arch_attr():
    machine_arch = generate_random_int(lower_bound=0, upper_bound=16)
    jt = JobTemplate()
    jt.machine_arch = machine_arch
    assert (jt.machine_arch == Cpu(machine_arch).name)
    print('\nJob template object with machine_arch: %s' % (machine_arch))


def test_start_time_attr():
    start_time = datetime.datetime.now()
    jt = JobTemplate()
    jt.start_time = start_time
    assert (int((jt.start_time - POSIX_EPOCH).total_seconds()) == int((start_time - POSIX_EPOCH).total_seconds()))
    print('\nJob template object with start_time: %s' % (start_time))


def test_deadline_time_attr():
    deadline_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    jt = JobTemplate()
    jt.deadline_time = deadline_time
    assert (int((jt.deadline_time - POSIX_EPOCH).total_seconds()) == int((deadline_time - POSIX_EPOCH).total_seconds()))
    print('\nJob template object with deadline_time: %s' % (deadline_time))


def test_stage_in_files_attr():
    stage_in_files = {}
    n_args = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_args):
        name = generate_random_string().upper()
        value = generate_random_string()
        stage_in_files[name] = value
    jt = JobTemplate()
    jt.stage_in_files = stage_in_files
    assert (jt.stage_in_files == stage_in_files)
    print('\nJob template object with stage_in_files: %s' % (stage_in_files))


def test_stage_out_files_attr():
    stage_out_files = {}
    n_args = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_args):
        name = generate_random_string().upper()
        value = generate_random_string()
        stage_out_files[name] = value
    jt = JobTemplate()
    jt.stage_out_files = stage_out_files
    assert (jt.stage_out_files == stage_out_files)
    print('\nJob template object with stage_out_files: %s' % (stage_out_files))


def test_resource_limits_attr():
    resource_limits = {}
    n_args = generate_random_int(lower_bound=1, upper_bound=5)
    for i in range(0, n_args):
        name = generate_random_string().upper()
        value = generate_random_string()
        resource_limits[name] = value
    jt = JobTemplate()
    jt.resource_limits = resource_limits
    assert (jt.resource_limits == resource_limits)
    print('\nJob template object with resource_limits: %s' % (resource_limits))


def test_accounting_id_attr():
    accounting_id = generate_random_string()
    jt = JobTemplate()
    jt.accounting_id = accounting_id
    assert (jt.accounting_id == accounting_id)
    print('\nJob template object with accounting_id: %s' % (accounting_id))


def test_implementation_specific_attr():
    implementation_specific = {}
    keys = JobTemplate.get_implementation_specific_keys()
    for k in keys:
        v = generate_random_string()
        implementation_specific[k] = v
    jt = JobTemplate()
    jt.implementation_specific = implementation_specific
    assert (jt.implementation_specific == implementation_specific)
    print('\nJob template object with implementation_specific: %s' % (implementation_specific))
