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

from .version import Version
from .drmaa2_object_descriptors import Drmaa2Descriptor

from .log_manager import LogManager


class Drmaa2VersionDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_version fields. """

    logger = LogManager.get_instance().get_logger('Drmaa2VersionDescriptor')

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        if not obj:
            return None
        if obj._struct is not None:
            ctypes_version = getattr(obj._struct.contents, self.name)
            py_version = Version(ctypes_version)
        return py_version

    def __set__(self, obj, ctypes_version):
        if not obj:
            return
            # setattr(obj._struct.contents, self.name, value)
