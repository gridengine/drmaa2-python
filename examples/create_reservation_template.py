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

from drmaa2 import ReservationTemplate

if __name__ == '__main__':
    import datetime

    print('Impl. spec. keys: %s' % ReservationTemplate.get_implementation_specific_keys())
    rt = ReservationTemplate({'reservation_name': 'res-01'})
    print('Initial reservation template: %s' % rt)
    rt.users_acl = ['user1', 'user2', 'user3']
    rt.min_slots = 2
    rt.machine_os = 'LINUX'
    rt.start_time = datetime.datetime.now()
    print('Current reservation template: %s' % rt)
    rt.set_impl_spec_key_value('uge_rt_native', 'xxx')
    print('Impl. spec. key uge_rt_native is set to: %s' % rt.get_impl_spec_key_value('uge_rt_native'))
    print('Impl. spec dictionary: %s' % rt.implementation_specific)
    print('Final reservation template: %s' % rt)
