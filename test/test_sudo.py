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

from .utils import generate_random_string
from .utils import generate_random_int
from drmaa2 import Sudo
from drmaa2 import Drmaa2Exception


def test_username_attr():
    username = generate_random_string()
    s = Sudo()
    s.username = username
    assert (s.username == username)
    s2 = Sudo(username=username)
    assert (s2.username == username)
    s3 = Sudo(sudo_dict={'username': username})
    assert (s3.username == username)
    print('\nSudo object with username: %s' % (username))


def test_groupname_attr():
    groupname = generate_random_string()
    s = Sudo()
    s.groupname = groupname
    assert (s.groupname == groupname)
    s2 = Sudo(groupname=groupname)
    assert (s2.groupname == groupname)
    s3 = Sudo(sudo_dict={'groupname': groupname})
    assert (s3.groupname == groupname)
    print('\nSudo object with groupname: %s' % (groupname))


def test_uid_attr():
    uid = generate_random_int()
    s = Sudo()
    s.uid = uid
    assert (s.uid == uid)
    s2 = Sudo(uid=uid)
    assert (s2.uid == uid)
    s3 = Sudo(sudo_dict={'uid': uid})
    assert (s3.uid == uid)
    print('\nSudo object with uid: %s' % (uid))


def test_gid_attr():
    gid = generate_random_int()
    s = Sudo()
    s.gid = gid
    assert (s.gid == gid)
    s2 = Sudo(gid=gid)
    assert (s2.gid == gid)
    s3 = Sudo(sudo_dict={'gid': gid})
    assert (s3.gid == gid)
    print('\nSudo object with gid: %s' % (gid))
