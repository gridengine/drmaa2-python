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

import random
from drmaa2 import ReservationSession


def test_get_info():
    rs = ReservationSession('rs-01')
    r_name = 'res-%s' % int(random.uniform(0, 1000))
    r = rs.request_reservation({'reservation_name': r_name, 'duration': 100})
    ri = r.get_info()
    assert (ri.reservation_name == r_name)
    r.terminate()
    print('\nGet info: %s' % (ri))


def test_terminate():
    rs = ReservationSession('rs-01')
    r_name = 'res-%s' % int(random.uniform(0, 1000))
    r = rs.request_reservation({'reservation_name': r_name, 'duration': 100})
    r.terminate()
    print('\nTerminate reservation: %s' % (r))


def test_get_template():
    rs = ReservationSession('rs-01')
    r_name = 'res-%s' % int(random.uniform(0, 1000))
    d = {'reservation_name': r_name, 'duration': 100}
    r = rs.request_reservation(d)
    rt = r.get_template()
    assert (rt.reservation_name == r_name)
    print('\nGet template: %s' % (rt))
