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
from ctypes import pointer

from .drmaa2_constants import Os
from .drmaa2_constants import Cpu
from .drmaa2_ctypes import drmaa2_rtemplate
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_object import Drmaa2Object
from .drmaa2_exceptions import InvalidArgument


class ReservationTemplate(Drmaa2Object):
    """ High-level DRMAA2 reservation template class. """

    reservation_name = Drmaa2Object.StringDescriptor('reservationName')
    """ Reservation name (str). """
    start_time = Drmaa2Object.TimeDescriptor('startTime')
    """ Reservation start time (datetime). """
    end_time = Drmaa2Object.TimeDescriptor('endTime')
    """ Reservation end time (datetime). """
    duration = Drmaa2Object.LongLongDescriptor('duration')
    """ Reservation duration (long). """
    min_slots = Drmaa2Object.LongLongDescriptor('minSlots')
    """ Minimum number of slots required by the job (long). """
    max_slots = Drmaa2Object.LongLongDescriptor('maxSlots')
    """ Maximum number of slots required by the job (long). """
    job_category = Drmaa2Object.StringDescriptor('jobCategory')
    """ Reservation category (str). """
    users_acl = Drmaa2Object.StringListDescriptor('usersACL')
    """ Arguments for the job executable ([str]). """
    candidate_machines = Drmaa2Object.StringListDescriptor('candidateMachines')
    """ List of machines that are candidate for running the job ([str]). """
    min_phys_memory = Drmaa2Object.LongLongDescriptor('minPhysMemory')
    """ Minimum physical memory needed for the job (long). """
    machine_os = Drmaa2Object.EnumDescriptor('machineOS', Os)
    """ OS required for the job (Os). """
    machine_arch = Drmaa2Object.EnumDescriptor('machineArch', Cpu)
    """ Machine arch required for the job (Cpu). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, template={}):
        """ 
        Constructor. 

        :param template: Input structure representing the object; this structure is typically a dictionary, but it can also be a low-level drmaa2_rtemplate struct.
        :type template: dict 

        :raises InvalidArgument: in case of an invalid input argument.
        :raises Drmaa2Exception: for all other errors.

        >>> rt = ReservationTemplate({'reservation_name' : 'res-01', 'users_acl' : ['user1', 'user2']})
        >>> print(rt.reservation_name)
        res-01
        >>> rt.min_slots = 2
        """
        Drmaa2Object.__init__(self)
        if isinstance(template, dict):
            self._struct = self.get_drmaa2_library().drmaa2_rtemplate_create()
            self.init_impl_spec_key_values()
            self.from_dict(template)
        elif isinstance(template, POINTER(drmaa2_rtemplate)):
            self._struct = template
        else:
            raise InvalidArgument('Invalid argument: %s' % str(template))

    def __del__(self):
        setattr(self._struct.contents, 'reservationName', drmaa2_string())
        setattr(self._struct.contents, 'jobCategory', drmaa2_string())
        self.get_drmaa2_library().drmaa2_rtemplate_free(pointer(self._struct))

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.

        >>> print(ReservationTemplate.get_implementation_specific_keys())
        ['uge_rt_native']
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(
                cls.get_drmaa2_library().drmaa2_rtemplate_impl_spec())
        return cls.implementation_specific_keys
