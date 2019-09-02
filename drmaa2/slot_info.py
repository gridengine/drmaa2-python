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

from ctypes import cast
from ctypes import POINTER

from .byte_string import ByteString
from .drmaa2_ctypes import drmaa2_slotinfo
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_object import Drmaa2Object


class SlotInfo(Drmaa2Object):
    """ High-level DRMAA2 slot info class. """

    machine_name = Drmaa2Object.StringDescriptor('machineName')
    """ Machine name (str). """
    slots = Drmaa2Object.LongLongDescriptor('slots')
    """ Number of slots (long). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, struct=None):
        """ Constructor. """
        Drmaa2Object.__init__(self)
        if struct is not None:
            self._struct = POINTER(drmaa2_slotinfo)()
            self._struct.contents = drmaa2_slotinfo()
            machine_name = ByteString(getattr(struct.contents, 'machineName').value).decode()
            # self.machine_name = ByteString(getattr(struct.contents, 'machineName').value).decode()
            self.machine_name = machine_name
            self.slots = getattr(struct.contents, 'slots')

    def __del__(self):
        pass

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.
        """
        if cls.implementation_specific_keys is None:
            # cls.implementation_specific_keys = cls.to_py_string_list(cls.get_drmaa2_library().drmaa2_slotinfo_impl_spec())
            cls.implementation_specific_keys = []
        return cls.implementation_specific_keys

    @classmethod
    def to_py_job_list(cls, ctypes_list):
        py_job_list = list()
        if ctypes_list:
            count = cls.drmaa2_lib.drmaa2_list_size(ctypes_list)
            cls.logger.debug('Converting ctypes job list of size {}'.format(count))
            for i in range(count):
                void_ptr = cls.drmaa2_lib.drmaa2_list_get(ctypes_list, i)
                if void_ptr:
                    si = cast(void_ptr, POINTER(drmaa2_slotinfo))
                    si = SlotInfo(si)
                    py_job_list.append(si)
                else:
                    ExceptionMapper.check_last_error_code()
                    py_job_list.append(None)
        return py_job_list

    @classmethod
    def to_ctypes_job_list(cls, py_job_list):
        cls.logger.debug('Converting py job list of size {}'.format(len(py_job_list)))
        ctypes_job_list = cls.drmaa2_lib.drmaa2_list_create(int(ListType.SLOTINFOLIST), drmaa2_list_entryfree())
        for si in py_job_list:
            ExceptionMapper.check_status_code(cls.drmaa2_lib.drmaa2_list_add(ctypes_job_list, si._struct))
        return ctypes_job_list
