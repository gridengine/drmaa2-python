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


def test_machine_info():
    h = socket.gethostname().split('.',1)[0] # use short name
    ms = MonitoringSession('ms-01')
    mi_list = ms.get_all_machines([h])
    print(mi_list)
    assert (len(mi_list) == 1)
    mi = mi_list[0]
    assert (mi.name == h)
    print('\nGot machine info: %s' % (mi.to_dict()))
