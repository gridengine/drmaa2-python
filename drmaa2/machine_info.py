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

from ctypes import POINTER
from ctypes import cast

from .byte_string import ByteString
from .drmaa2_constants import Cpu
from .drmaa2_constants import Os
from .drmaa2_ctypes import drmaa2_machineinfo
from .drmaa2_object import Drmaa2Object
from .drmaa2_exceptions import InvalidArgument

from .drmaa2_version_descriptor import Drmaa2VersionDescriptor


class MachineInfo(Drmaa2Object):
    """ High-level DRMAA2 machine info class. """

    name = Drmaa2Object.StringDescriptor('name')
    """ Machine name (str). """
    available = Drmaa2Object.BoolDescriptor('available')
    """ Available flag (bool). """
    sockets = Drmaa2Object.LongLongDescriptor('sockets')
    """ Number of sockets (long). """
    cores_per_socket = Drmaa2Object.LongLongDescriptor('coresPerSocket')
    """ Number of cores per socket (long). """
    threads_per_core = Drmaa2Object.LongLongDescriptor('threadsPerCore')
    """ Number of threads per core (long). """
    load = Drmaa2Object.FloatDescriptor('load')
    """ Machine load (float). """
    phys_memory = Drmaa2Object.LongLongDescriptor('physMemory')
    """ Physical memory (long). """
    virt_memory = Drmaa2Object.LongLongDescriptor('virtMemory')
    """ Virtual memory (long). """
    machine_arch = Drmaa2Object.EnumDescriptor('machineArch', Cpu)
    """ Architecture (Cpu). """
    machine_os_version = Drmaa2VersionDescriptor('machineOSVersion')
    """ Operating system version (Version). """
    machine_os = Drmaa2Object.EnumDescriptor('machineOS', Os)
    """ Operating system (Os). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, machine_info):
        """ 
        Constructor. 

        :param machine_info: Low-level drmaa2_machineinfo struct.
        :type machine_info: drmaa2_machineinfo
        """
        Drmaa2Object.__init__(self)
        if isinstance(machine_info, POINTER(drmaa2_machineinfo)):
            self._struct = POINTER(drmaa2_machineinfo)()
            self._struct.contents = drmaa2_machineinfo()
            self.name = ByteString(getattr(machine_info.contents, 'name').value).decode()
            self.available = getattr(machine_info.contents, 'available')
            self.sockets = getattr(machine_info.contents, 'sockets')
            self.cores_per_socket = getattr(machine_info.contents, 'coresPerSocket')
            self.threads_per_core = getattr(machine_info.contents, 'threadsPerCore')
            self.load = getattr(machine_info.contents, 'load')
            self.phys_memory = getattr(machine_info.contents, 'physMemory')
            self.virt_memory = getattr(machine_info.contents, 'virtMemory')
            self.machine_arch = getattr(machine_info.contents, 'machineArch')
            self.machine_os_version = getattr(machine_info.contents, 'machineOSVersion')
            self.machine_os = getattr(machine_info.contents, 'machineOS')
            self.implementation_specific = getattr(machine_info.contents, 'implementationSpecific')
        else:
            raise InvalidArgument('Invalid argument: %s' % str(machine_info))
        self._read_only = True

    def __del__(self):
        pass

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.

        >>> print(MachineInfo.get_implementation_specific_keys())
        []
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(
                cls.get_drmaa2_library().drmaa2_machineinfo_impl_spec())
        return cls.implementation_specific_keys

    @classmethod
    def to_py_machine_info_list(cls, ctypes_list):
        drmaa2_lib = cls.get_drmaa2_library()
        py_machine_info_list = list()
        if ctypes_list:
            count = drmaa2_lib.drmaa2_list_size(ctypes_list)
            cls.logger.debug('Converting ctypes machine info list of size {}'.format(count))
            for i in range(count):
                void_ptr = drmaa2_lib.drmaa2_list_get(ctypes_list, i)
                if void_ptr:
                    mi = cast(void_ptr, POINTER(drmaa2_machineinfo))
                    mi = MachineInfo(mi)
                    py_machine_info_list.append(mi)
                else:
                    ExceptionMapper.check_last_error_code()
                    # py_machine_info_list.append(None)
        return py_machine_info_list
