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

from drmaa2 import JobSession

if __name__ == '__main__':
    js = JobSession('js-01')
    print('Created job session: %s' % js.name)
    d = {'remote_command': '/bin/sleep', 'args': ['10']}
    print('Running job array using dictionary: %s' % d)
    begin_index = 1
    end_index = 10
    step = 2
    max_parallel = 2
    ja = js.run_bulk_jobs(d, begin_index, end_index, step, max_parallel)
    print('Submitted job array: %s' % ja)
    print('Waiting for any job to terminate')
    jl = ja.job_list
    j = js.wait_any_terminated(jl)
    print('Job %s terminated' % j)
