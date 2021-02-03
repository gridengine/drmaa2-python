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

from drmaa2 import JobTemplate

if __name__ == '__main__':
    import datetime

    print('Impl. spec. keys: %s' % JobTemplate.get_implementation_specific_keys())
    jt = JobTemplate({'remote_command': '/bin/sleep'})
    print('Initial job template: %s' % jt)
    jt.args = ['200']
    jt.job_environment = {'MY_ENV': 'xyz', 'MY_ENV2': 'xyz2'}
    jt.rerunnable = True
    jt.submit_as_hold = True
    jt.queue_name = 'all.q'
    jt.min_slots = 2
    jt.machine_os = 'LINUX'
    jt.start_time = datetime.datetime.now()
    jt.working_directory = '/tmp'
    print('Current job template: %s' % jt)
    jt.set_impl_spec_key_value('uge_jt_pe', 'xxx')
    print('Impl. spec. key uge_jt_pe is set to: %s' % jt.get_impl_spec_key_value('uge_jt_pe'))
    print('Impl. spec dictionary: %s' % jt.implementation_specific)
    print('Final job template: %s' % jt)
