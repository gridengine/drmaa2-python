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

"""
Sudo class.
"""

from ctypes import POINTER
from .drmaa2_ctypes import drmaa2_sudo
from .drmaa2_object import Drmaa2Object


class Sudo(Drmaa2Object):
    """ High-level DRMAA2 sudo class. """

    username = Drmaa2Object.CharBufferDescriptor('username')
    """ Username to run operation as (str). """
    groupname = Drmaa2Object.CharBufferDescriptor('groupname')
    """ Groupname to run operation as (str). """
    uid = Drmaa2Object.LongDescriptor('uid')
    """ User id to run operation as (int). """
    gid = Drmaa2Object.LongDescriptor('gid')
    """ Group id to run operation as (int). """

    def __init__(self, username=None, groupname=None, uid=None, gid=None, sudo_dict={}):
        """ 
        Constructor. 

        :param username: Sudo object username; it may be also be specified as part of the sudo object dictionary.
        :type username: str
 
        :param groupname: Sudo object groupname; it may be also be specified as part of the sudo object dictionary.
        :type groupname: str
 
        :param uid: Sudo object user id; it may be also be specified as part of the sudo object dictionary.
        :type uid: int
 
        :param gid: Sudo object group id; it may be also be specified as part of the sudo object dictionary.
        :type gid: int
 
        :param sudo_dict: Sudo object dictionary; if specified, it should contain 'username', 'groupname', 'uid' and/or 'gid' keys.
        :type sudo_dict: dict

        >>> auth = Sudo(username='auser', groupname='agroup')
        >>> print('Username: %s' % auth.username)
        >>> Username: auser
        """
        Drmaa2Object.__init__(self)
        self._struct = POINTER(drmaa2_sudo)()
        self._struct.contents = drmaa2_sudo()

        username = username or sudo_dict.get('username')
        self.username = username
        self.groupname = groupname or sudo_dict.get('groupname')
        self.uid = uid or sudo_dict.get('uid')
        self.gid = gid or sudo_dict.get('gid')

    def __del__(self):
        pass
