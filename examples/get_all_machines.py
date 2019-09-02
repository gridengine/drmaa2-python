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

import socket
from drmaa2 import MonitoringSession

if __name__ == '__main__':
    ms = MonitoringSession('ms-01')
    print('Opened monitoring session: %s' % ms.name)
    hostname = socket.gethostname()
    print('Retrieving machine information for host %s' % hostname)
    mi_list = ms.get_all_machines([hostname])
    print('Got all machines: %s' % mi_list)
