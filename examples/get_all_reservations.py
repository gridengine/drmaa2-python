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

import random
from drmaa2 import ReservationInfo
from drmaa2 import ReservationSession
from drmaa2 import MonitoringSession

if __name__ == '__main__':
    rs = ReservationSession('rs-01')
    print('Created reservation session: %s' % rs.name)
    r_name = 'res-%s' % int(random.uniform(0, 1000))
    d = {'reservation_name' : r_name, 'duration' : 100}
    r = rs.request_reservation(d)
    print('Created reservation: %s' % r)
    #ri = r.get_info()
    ri = ReservationInfo({'reservation_name' : r_name})
    # At the moment one cannot have both reservation and monitoring 
    # sessions opened at the same time
    rs.close()

    ms = MonitoringSession('ms-01')
    print('Opened monitoring session: %s' % ms.name)
    print('Retrieving reservations matching reservation info %s' % ri)
    r_list = ms.get_all_reservations(ri)
    print('Got all reservations: %s' % r_list)

