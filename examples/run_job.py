#!/usr/bin/env python 
#___INFO__MARK_BEGIN__
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
#___INFO__MARK_END__

from drmaa2 import JobSession
from drmaa2 import JobTemplate

if __name__ == '__main__':
    js = JobSession('js-01')
    print('Created job session: %s' % js.name)
    d = {'remote_command' : '/bin/sleep', 'args' : ['100']}
    print('Running job using dictionary: %s' % d)
    j = js.run_job(d)
    print('Submitted job: %s' % j)

    jt = JobTemplate({'remote_command' : '/bin/sleep', 'args' : ['100']})
    print('\nRunning job using template: %s' % jt)
    j2 = js.run_job(jt)
    print('Submitted job: %s' % j2)


