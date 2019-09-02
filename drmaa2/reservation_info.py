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

from .drmaa2_ctypes import drmaa2_rinfo
from .drmaa2_object import Drmaa2Object
from .drmaa2_exceptions import InvalidArgument


class ReservationInfo(Drmaa2Object):
    """ High-level DRMAA2 reservation info class. """

    reservation_id = Drmaa2Object.StringDescriptor('reservationId')
    """ Reservation id (str). """
    reservation_name = Drmaa2Object.StringDescriptor('reservationName')
    """ Reservation name (str). """
    reserved_start_time = Drmaa2Object.TimeDescriptor('reservedStartTime')
    """ Reserved start time (datetime). """
    reserved_end_time = Drmaa2Object.TimeDescriptor('reservedEndTime')
    """ Reserved end time (datetime). """
    users_acl = Drmaa2Object.StringListDescriptor('usersACL')
    """ Users ACL ([str]). """
    reserved_slots = Drmaa2Object.LongLongDescriptor('reservedSlots')
    """ Reserved slots (long). """
    reserved_machines = Drmaa2Object.StringListDescriptor('reservedMachines')
    """ Reserved machines ([str]). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, reservation_info={}):
        """ 
        Constructor. 

        :param reservation_info: Input structure representing the object; this structure is typically a dictionary, but it can also be a low-level drmaa2_rinfo struct.
        :type reservation_info: dict 

        :raises InvalidArgument: in case of an invalid input argument.
        :raises Drmaa2Exception: for all other errors.

        >>> ri = ReservationInfo({'reservation_name' : 'sv-01'})
        >>> print(ri.reservation_name)
        sv-01
        >>> ri.reserved_slots = 3
        """
        Drmaa2Object.__init__(self)
        if isinstance(reservation_info, dict):
            self._struct = self.get_drmaa2_library().drmaa2_rinfo_create()
            self.init_impl_spec_key_values()
            self.from_dict(reservation_info)
        elif isinstance(reservation_info, POINTER(drmaa2_rinfo)):
            self._struct = reservation_info
        else:
            raise InvalidArgument('Invalid argument: %s' % str(reservation_info))

    def __del__(self):
        # self.get_drmaa2_library().drmaa2_rinfo_free(pointer(self._struct))
        pass

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.

        >>> print(ReservationInfo.get_implementation_specific_keys())
        ['uge_ri_ar_json']
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(cls.get_drmaa2_library().drmaa2_rinfo_impl_spec())
        return cls.implementation_specific_keys
