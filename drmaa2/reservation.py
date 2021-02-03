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

from ctypes import cast
from ctypes import POINTER

from .drmaa2_constants import ListType
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_r
from .drmaa2_ctypes import drmaa2_list_entryfree

from .sudo import Sudo

from .reservation_template import ReservationTemplate
from .reservation_info import ReservationInfo

from .byte_string import ByteString
from .drmaa2_object import Drmaa2Object
from .log_manager import LogManager
from .exception_mapper import ExceptionMapper


class Reservation(Drmaa2Object):
    """ High-level DRMAA2 reservation class. """

    id = Drmaa2Object.StringDescriptor('id')
    """ Reservation id (str). """
    session_name = Drmaa2Object.StringDescriptor('session_name')
    """ Session name (str). """

    logger = LogManager.get_instance().get_logger('Reservation')

    def __init__(self, reservation):
        """ Constructor. """
        Drmaa2Object.__init__(self)
        if isinstance(reservation, POINTER(drmaa2_r)):
            self._struct = POINTER(drmaa2_r)()
            self._struct.contents = drmaa2_r()
            self.id = ByteString(getattr(reservation.contents, 'id').value).decode()
            self.session_name = ByteString(getattr(reservation.contents, 'session_name').value).decode()
        else:
            raise InvalidArgument('Invalid argument: %s' % str(reservation))

    def terminate(self, auth=None):
        """ 
        Terminate the reservation.

        :param auth: Optional sudo object for terminating the reservation; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> r = r_session.request_reservation({'reservation_name' : 'res-01', 'duration' : 100})
        >>> ...
        >>> r.terminate()
        """
        self.logger.debug('Terminating reservation id {}'.format(self.id))
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(self.drmaa2_lib.drmaa2_r_terminate_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(self.drmaa2_lib.drmaa2_r_terminate(self._struct))

    def get_template(self):
        """ 
        Get reservation template.

        :returns: ReservationTemplate object.

        >>> r = r_session.request_reservation({'reservation_name' : 'res-01', 'duration' : 100})
        >>> ...
        >>> rt = r.get_template()
        >>> print(rt.users_acl)
        []
        """
        self.logger.debug('Retrieving template for reservation id {}'.format(self.id))
        # ctypes_reservation_template = self.drmaa2_lib.drmaa2_r_get_reservation_template(self._struct)
        ctypes_reservation_template = self.drmaa2_lib.drmaa2_r_get_rtemplate(self._struct)
        if not ctypes_reservation_template:
            ExceptionMapper.check_last_error_code()

        return ReservationTemplate(ctypes_reservation_template)

    def get_info(self):
        """ 
        Get reservation info.

        :returns: ReservationInfo object.

        >>> r = r_session.request_reservation({'reservation_name' : 'res-01', 'duration' : 100})
        >>> ...
        >>> ri = r.get_info()
        >>> print(ri.users_acl)
        []
        """
        self.logger.debug('Retrieving info for reservation id {}'.format(self.id))
        ctypes_reservation_info = self.drmaa2_lib.drmaa2_r_get_info(self._struct)
        if not ctypes_reservation_info:
            ExceptionMapper.check_last_error_code()
        return ReservationInfo(ctypes_reservation_info)

    def __del__(self):
        pass

    @classmethod
    def to_py_reservation_list(cls, ctypes_list):
        py_reservation_list = list()
        if ctypes_list:
            count = cls.drmaa2_lib.drmaa2_list_size(ctypes_list)
            cls.logger.debug('Converting ctypes reservation list of size {}'.format(count))
            for i in range(count):
                void_ptr = cls.drmaa2_lib.drmaa2_list_get(ctypes_list, i)
                if void_ptr:
                    r = cast(void_ptr, POINTER(drmaa2_r))
                    r = Reservation(r)
                    py_reservation_list.append(r)
                else:
                    ExceptionMapper.check_last_error_code()
                    py_reservation_list.append(None)
        return py_reservation_list

    @classmethod
    def to_ctypes_reservation_list(cls, py_reservation_list):
        cls.logger.debug('Converting py reservation list of size {}'.format(len(py_reservation_list)))
        ctypes_reservation_list = cls.drmaa2_lib.drmaa2_list_create(int(ListType.RESERVATIONLIST),
                                                                    drmaa2_list_entryfree())
        for r in py_reservation_list:
            ExceptionMapper.check_status_code(cls.drmaa2_lib.drmaa2_list_add(ctypes_reservation_list, j._struct))
        return ctypes_reservation_list
