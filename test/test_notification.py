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

from nose import SkipTest
from drmaa2 import Notification
from drmaa2 import UnsupportedOperation


def test_register_event_callback():
    def callback(notification):
        print('Got notification: %s' % notification)

    try:
        Notification.register_event_notification(callback)
        print('\nRegistered callback for event notification')
    except UnsupportedOperation:
        raise SkipTest('Not yet implemented optional feature.')
