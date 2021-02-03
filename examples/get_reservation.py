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

import random
from drmaa2 import ReservationSession

if __name__ == '__main__':
    rs = ReservationSession('rs-01')
    print('Created reservation session: %s' % rs.name)
    r_name = 'res-%s' % int(random.uniform(0, 1000))
    d = {'reservation_name': r_name, 'duration': 100}
    print('Requesting reservation using dictionary: %s' % d)
    r = rs.request_reservation(d)
    print('Created reservation: %s' % r)
    r_id = r.id
    print('Retrieving reservation id: %s' % r_id)
    r2 = rs.get_reservation(r_id)
    print('Retrieved reservation: %s' % r2)
