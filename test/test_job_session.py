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

import random
from .utils import generate_random_string
from .utils import needs_uge
from drmaa2 import JobSession
from drmaa2 import JobInfo


@needs_uge
def test_list_session_names():
    session_names = JobSession.list_session_names()
    assert (type(session_names) == type([]))
    print('\nThere are %s existing sessions: %s' % (len(session_names), session_names))


def test_new_session():
    session_name = generate_random_string()
    existing_session_names = JobSession.list_session_names()
    js = JobSession(session_name)
    session_names = JobSession.list_session_names()
    assert (len(session_names) == len(existing_session_names) + 1)
    print('\nCreated new session: %s' % (session_name))


def test_existing_session():
    session_name = generate_random_string()
    existing_session_names = JobSession.list_session_names()
    js = JobSession(session_name, destroy_on_exit=False)
    session_names = JobSession.list_session_names()
    assert (len(session_names) == len(existing_session_names) + 1)
    print('\nCreated new session: %s' % (session_name))
    del js
    js = JobSession(session_name)
    session_names2 = JobSession.list_session_names()
    assert (len(session_names) == len(session_names2))
    print('Opened existing session: %s' % (session_name))
    del js
    session_names3 = JobSession.list_session_names()
    assert (len(session_names3) == len(existing_session_names))
    print('Closed session: %s' % (session_name))


def test_destroy_session():
    session_names = JobSession.list_session_names()
    print('\nExisting session names: %s' % session_names)
    for name in session_names:
        print('Destroying session: %s' % name)
        JobSession.destroy_by_name(name)
    session_names = JobSession.list_session_names()
    print('Remaining session names: %s' % session_names)
    assert (len(session_names) == 0)


def test_run_job():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    j = js.run_job(d)
    j_id = j.id
    assert (len(j_id) > 0)
    print('\nSubmitted job id: %s' % j_id)


def test_run_bulk_jobs():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 5, 2)
    jl = ja.job_list
    ja_id = ja.id
    assert (len(ja_id) > 0)
    assert (len(jl) == 2)
    print('\nSubmitted job array id: %s' % ja_id)


def test_wait_any_started():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 5, 2)
    jl = ja.job_list
    jl_ids = list(map(lambda j: j.id, jl))
    print('\nWaiting on start of any job with id from %s' % jl_ids)
    j = js.wait_any_started(jl)
    assert (j.id in jl_ids)
    print('Job %s started' % j)


def test_wait_any_terminated():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 5, 2)
    jl = ja.job_list
    jl_ids = list(map(lambda j: j.id, jl))
    print('\nWaiting on termination of any job with id from %s' % jl_ids)
    j = js.wait_any_terminated(jl)
    assert (j.id in jl_ids)
    print('Job %s terminated' % j)


def test_wait_all_started():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 5, 2)
    jl = ja.job_list
    jl_ids = list(map(lambda j: j.id, jl))
    jl_ids.sort()
    print('\nWaiting on start of all jobs: %s' % jl_ids)
    jl2 = js.wait_all_started(jl)
    jl2_ids = list(map(lambda j: j.id, jl2))
    jl2_ids.sort()
    assert (jl_ids == jl2_ids)
    print('Jobs started: ' % jl2_ids)


def test_wait_all_terminated():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 5, 2)
    jl = ja.job_list
    jl_ids = list(map(lambda j: j.id, jl))
    jl_ids.sort()
    print('\nWaiting on termination of all jobs: %s' % jl_ids)
    jl2 = js.wait_all_terminated(jl)
    jl2_ids = list(map(lambda j: j.id, jl2))
    jl2_ids.sort()
    assert (jl_ids == jl2_ids)
    print('Jobs terminated: ' % jl2_ids)


def test_get_job_array():
    session_name = generate_random_string()
    js = JobSession(session_name)
    d = {'remote_command': '/bin/sleep', 'args': ['5'], 'output_path': '/dev/null', 'join_files': True}
    ja = js.run_bulk_jobs(d, 1, 10, 5, 2)
    ja2 = js.get_job_array(ja.id)
    assert (ja.id == ja2.id)
    print('\nRetrieved job array: %s' % ja2)


def test_get_job_categories():
    session_name = generate_random_string()
    js = JobSession(session_name)
    job_categories = js.get_job_categories()
    assert (type(job_categories) == type([]))
    print('\nThere are %s job categories: %s' % (len(job_categories), job_categories))


def test_get_jobs():
    js = JobSession('js-01')
    j_name = 'drmaa2python-%s' % int(random.uniform(0, 1000))
    d = {'remote_command': '/bin/sleep', 'args': ['10'], 'job_name': j_name, 'output_path': '/dev/null', 'join_files': True}
    j = js.run_job(d)
    print('\nSubmitted job: %s' % j)
    ji = j.get_info()
    print('Retrieving jobs matching job info %s' % ji)
    ji2 = JobInfo({'job_id': ji.job_id})
    j_list = js.get_jobs(ji2)
    print('Got jobs: %s' % j_list)
    assert (len(j_list) >= 1)
