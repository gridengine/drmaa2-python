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
from drmaa2 import ReservationInfo

if __name__ == '__main__':
    print('Impl. spec. keys: %s' % ReservationInfo.get_implementation_specific_keys())
    ri = ReservationInfo({'reservation_name': 'rs-01'})
    print('Initial reservation info: %s' % ri)
    ri.reservation_id = 'rid-01'
    ri.users_acl = ['user1', 'user2', 'user3']
    ri.reserved_start_time = datetime.datetime.now()
    ri.reserved_end_time = datetime.datetime.now()
    ri.reserved_slots = 5
    ri.set_impl_spec_key_value('uge_ri_ar_json ', 'UGE RI AR JSON')
    print('Impl. spec. key uge_ri_ar_json is set to: %s' % ri.get_impl_spec_key_value('uge_ri_ar_json'))
    print('Impl. spec dictionary: %s' % ri.implementation_specific)
    print('Final reservation info: %s' % ri)
