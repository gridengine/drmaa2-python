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

import random
from drmaa2 import JobSession
from drmaa2 import JobInfo
from drmaa2 import MonitoringSession

if __name__ == '__main__':
    js = JobSession('js-01')
    print('Created job session: %s' % js.name)
    j_name = 'job-%s' % int(random.uniform(0, 1000))
    j = js.run_job({'remote_command': '/bin/sleep', 'args': ['10'], 'job_name': j_name})
    print('Submitted job: %s' % j)
    # ji = j.get_info()
    ji = JobInfo({'job_name': j_name})
    ms = MonitoringSession('ms-01')
    print('Opened monitoring session: %s' % ms.name)
    print('Retrieving jobs matching job info %s' % ji)
    j_list = ms.get_all_jobs(ji)
    print('Got all jobs: %s' % j_list)
