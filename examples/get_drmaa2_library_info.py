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

from drmaa2 import Capability
from drmaa2 import Version
from drmaa2 import LibraryManager

# The following are also available as drmaa2 module methods
#get_drms_name 
#get_drmaa_name
#drmaa_supports
#get_drms_version
#get_drmaa_version
#get_job_session_names
#get_reservation_session_names

if __name__ == '__main__':
    lm = LibraryManager.get_instance()
    print('Got library manager')
    drms_name = lm.get_drms_name()
    print('DRMS Name: %s' % drms_name)
    drmaa_name = lm.get_drmaa_name()
    print('DRMAA Name: %s' % drmaa_name)
    for c in Capability:
        print('Support for %s: %s' % (c, lm.drmaa_supports(c)))
    drms_version = Version.get_drms_version()
    print('DRMS Version: %s' % drms_version)
    drmaa_version = Version.get_drmaa_version()
    print('DRMAA Version: %s' % drmaa_version)


