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

import platform
from .drmaa2_constants import PY_STRING_TYPE


class ByteString:
    python_version = platform.python_version_tuple()[0]

    def __init__(self, s=''):
        if isinstance(s, ByteString):
            self.s = s.s
        self.s = s

    def __str__(self):
        return str(self.s)

    def encode(self):
        if self.s is None or self.python_version == '2':
            return self.s
        else:
            try:
                return self.s.encode()
            except AttributeError:
                return self.s

    def decode(self):
        if self.s is None or self.python_version == '2':
            return self.s
        else:
            try:
                return self.s.decode()
            except AttributeError:
                return self.s
