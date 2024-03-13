#!/usr/bin/env python
# ___INFO__MARK_BEGIN__
#######################################################################################
# Copyright 2008-2022 Altair Engineering Inc.
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

import time
from drmaa2 import JobSession
from drmaa2 import JobInfo
from drmaa2 import Time

if __name__ == '__main__':
    js = JobSession('js-01')
    print('Created job session: %s' % js.name)
    j = js.run_job({'remote_command': '/bin/sleep', 'args': ['100']})
    print('Submitted job: %s, waiting on start' % j)
    t1 = time.time()
    j.wait_started(10)
    t2 = time.time()
    print('Wait on job start is over after %s seconds' % (t2 - t1))
    ji = j.get_info()
    print('Retrieved job info: %s' % ji)
    print('Waiting on job %s termination' % j.id)
    t1 = time.time()
    j.wait_terminated(Time.INFINITE_TIME.value)
    t2 = time.time()
    print('Job terminated, wait is over after %s seconds' % (t2 - t1))
    ji = j.get_info()
    print('Retrieved job info after termination: %s' % ji)
