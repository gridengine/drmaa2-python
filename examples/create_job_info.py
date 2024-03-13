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

import datetime
from drmaa2 import JobInfo

if __name__ == '__main__':

    print('Impl. spec. keys: %s' % JobInfo.get_implementation_specific_keys())
    ji = JobInfo({'queue_name': 'all.q'})
    print('Initial job info: %s' % ji)
    ji.job_id = '113'
    ji.job_name = 'job-01'
    ji.slots = 10
    ji.job_owner = 'a.user'
    ji.submission_time = datetime.datetime.now()
    ji.cpu_time = 77
    ji.set_impl_spec_key_value('uge_ji_priority', '23')
    print('Impl. spec. key uge_ji_priority is set to: %s' % ji.get_impl_spec_key_value('uge_ji_priority'))
    print('Impl. spec dictionary: %s' % ji.implementation_specific)
    print('Final job info: %s' % ji)
