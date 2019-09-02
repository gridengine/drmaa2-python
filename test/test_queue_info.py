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

import os
from drmaa2 import MonitoringSession


def test_queue_info():
    q_name_list = os.popen('qconf -sql').read().split()
    print('\nGot queue list: %s' % q_name_list)
    ms = MonitoringSession('ms-01')
    qi_list = ms.get_all_queues(q_name_list)
    assert (len(qi_list) > 0)
    for qi in qi_list:
        q_name = qi.name
        print('\nChecking queue: %s' % (qi.to_dict()))
        assert (q_name in q_name_list)
