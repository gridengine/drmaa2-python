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

from .utils import generate_random_string
from drmaa2 import JobSession
from drmaa2 import JobState


def test_get_info():
    session_name = 'drmaa2python-%s' % generate_random_string()
    js = JobSession(session_name)
    job_name = 'drmaa2python-%s' % generate_random_string()
    d = {'remote_command': '/bin/sleep', 'args': ['10'], 'job_name': job_name}
    j = js.run_job(d)
    ji = j.get_info()
    assert (ji.job_name == job_name)
    print('\nGet info: %s' % (ji))


def test_wait_terminated():
    session_name = 'drmaa2python-%s' % generate_random_string()
    js = JobSession(session_name)
    job_name = 'drmaa2python-%s' % generate_random_string()
    d = {'remote_command': '/bin/sleep', 'args': ['10'], 'job_name': job_name}
    j = js.run_job(d)
    j.wait_terminated()
    s, ss = j.get_state()
    assert (s == JobState.DONE)
    print('\nWait terminated for job: %s' % (j))
    ji = j.get_info()
    print('\nGet info: %s' % (ji))
