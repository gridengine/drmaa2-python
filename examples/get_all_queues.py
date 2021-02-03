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

from drmaa2 import MonitoringSession

if __name__ == '__main__':
    ms = MonitoringSession('ms-01')
    print('Opened monitoring session: %s' % ms.name)
    q_name = 'all.q'
    print('Retrieving queue information for %s' % q_name)
    qi_list = ms.get_all_queues([q_name])
    print('Got all queues: %s' % qi_list)
