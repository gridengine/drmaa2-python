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

import getpass
from uuid import uuid4
from ctypes import pointer
from ctypes import c_void_p

from .byte_string import ByteString
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_object import Drmaa2Object

from .sudo import Sudo
from .reservation_template import ReservationTemplate
from .reservation import Reservation
from .log_manager import LogManager
from .exception_mapper import ExceptionMapper
from .drmaa2_exceptions import Drmaa2Exception


class ReservationSession(Drmaa2Object):
    """ High-level DRMAA2 reservation session class. """

    name = Drmaa2Object.StringDescriptor('name')
    """ Reservation session name (str). """
    contact = Drmaa2Object.StringDescriptor('contact')
    """ Reservation session contact (str). """

    logger = LogManager.get_instance().get_logger('ReservationSession')
    exception_mapper = ExceptionMapper()

    def __init__(self, name=None, contact=None, destroy_on_exit=True, check_for_existing_session=True, session_dict={}, auth=None):
        """ 
        Constructor. If the session with a given name does not already exist, 
        it will create a new one; otherwise, it will open the existing session.

        :param name: Session name; it may be also be specified as part of the reservation session object dictionary. If not provided, a random name will be used.
        :type name: str

        :param contact: Session contact; it may be also be specified as part of the reservation session object dictionary.
        :type contact: str

        :param destroy_on_exit: Destroy session when the reservation session object goes out of scope.
        :type destroy_on_exit: bool

        :param check_for_existing_session: If false, the constructor will not check for existing session with the given name.
        :type check_for_existing_session: bool

        :param session_dict: Reservation session dictionary; if specified, it should contain 'name' and (optionally) 'contact' keys.
        :type session_dict: dict

        :param auth: Optional sudo object for creating the session; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> r_session = ReservationSession()
        >>> print(r_session.name)
        def678952a654dfda75ffabae6890be
        """
        Drmaa2Object.__init__(self)
        self._destroy_on_exit = destroy_on_exit
        name = name or session_dict.get('name')
        if not name:
            name = uuid4().hex
            check_for_existing_session = False
        contact = contact or session_dict.get('contact') or drmaa2_string()
        create_new_session = True
        if check_for_existing_session:
             existing_session_names = self.list_session_names()
             session_names_to_check = [name]
             if contact:
                 session_names_to_check.append('%s@%s' % (contact,name))
             else:
                 session_names_to_check.append('%s@%s' % (getpass.getuser(),name))
             for n in session_names_to_check:
                 if n in existing_session_names:
                     name = n
                     self.logger.debug('Discovered existing job session with name {}'.format(n))
                     create_new_session = False
                     break

        self._name_bs = ByteString()
        self._auth = auth
        if create_new_session:
            self._struct = self.__create(name, contact, auth)
        else:
            self._struct = self.__open(name)
        self._struct_p = pointer(self._struct)
        self._name_bs = ByteString(name)
        self._read_only = True

    @classmethod
    def list_session_names(cls):
        """ 
        List existing sessions. 

        :returns: List of existing reservation session names.

        >>> print(ReservationSession.list_session_names())
        ['auser@rs-01']

        """
        return Drmaa2Object.to_py_string_list(cls.get_drmaa2_library().drmaa2_get_rsession_names())

    def __create(self, name, contact, auth):
        self.logger.debug('Creating reservation session with name {} (contact: {})'.format(name, contact))
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            struct = self.get_drmaa2_library().drmaa2_create_rsession_as(auth._struct, ByteString(name).encode(), ByteString(contact).encode())
        else:
            struct = self.get_drmaa2_library().drmaa2_create_rsession(ByteString(name).encode(), ByteString(contact).encode())
        if not struct:
            self.exception_mapper.check_last_error_code()
        return struct

    def __open(self, name):
        self.logger.debug('Opening reservation session {}'.format(name))
        struct = self.get_drmaa2_library().drmaa2_open_rsession(ByteString(name).encode())
        if not struct:
            self.exception_mapper.check_last_error_code()
        return struct

    def open(self):
        """ 
        Open session. This method is called automatically in the constructor.

        >>> ...
        >>> r_session.close()
        >>> ...
        >>> r_session.open()
        """
        if self._struct:
            self.logger.debug('Reservation session {} is already open'.format(self._name_bs.decode()))
        else:
            self._struct = self.__open(self._name_bs)
            self._struct_p = pointer(self._struct)

    def close(self):
        """ 
        Close session. This method is called automatically when the session
        object goes out of scope.

        >>> ...
        >>> r_session.close()
        """
        if self._struct:
            self.logger.debug('Closing reservation session {}'.format(self._name_bs.decode()))
            drmaa2_lib = self.get_drmaa2_library()
            self.exception_mapper.check_status_code(drmaa2_lib.drmaa2_close_rsession(self._struct))
            drmaa2_lib.drmaa2_rsession_free(self._struct_p)
            self._struct = None

    def destroy(self, auth=None):
        """ 
        Destroy session. This method is called automatically when the 
        session object goes out of scope, unless the destroy_on_exit flag is set to false.

        :param auth: Optional sudo object for destroying the session; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ...
        >>> r_session.destroy()
        """
        self.logger.debug('Destroying reservation session {}'.format(self._name_bs.decode()))
        auth = auth or self._auth
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            self.exception_mapper.check_status_code(self.get_drmaa2_library().drmaa2_destroy_rsession_as(auth._struct, self._name_bs.encode()))
        else:
            self.exception_mapper.check_status_code(self.get_drmaa2_library().drmaa2_destroy_rsession(self._name_bs.encode()))

    @classmethod
    def destroy_by_name(cls, name, auth=None):
        """ 
        Destroy session by name. 

        :param name: Session name.
        :type name: str

        :param auth: Optional sudo object for destroying the session; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ReservationSession.destroy_by_name('rs-01')
        """
        cls.logger.debug('Destroying reservation session {}'.format(name))
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            cls.exception_mapper.check_status_code(cls.get_drmaa2_library().drmaa2_destroy_rsession_as(auth._struct, ByteString(name).encode()))
        else:
            cls.exception_mapper.check_status_code(cls.get_drmaa2_library().drmaa2_destroy_rsession(ByteString(name).encode()))

    def __del__(self):
        """ Destructor. """
        self.close()
        if self._destroy_on_exit:
            try:
                self.destroy()
            except Drmaa2Exception as ex:
                self.logger.warn('Could not destroy reservation session: {}'.format(str(ex)))
        else:
            self.logger.debug('Will not destroy reservation session {}'.format(self._name_bs.decode()))
        if self._struct:
            self.get_drmaa2_library().drmaa2_rsession_free(self._struct_p)

    def request_reservation(self, template, auth=None):
        """ 
        Request reservation. 

        :param template: Reservation template; it can be specified either as a dictionary, or directly as a ReservationTemplate object.
        :type template: ReservationTemplate or dict

        :param auth: Optional sudo object for requesting the reservation; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        :returns: Reservation object.

        >>> r = r_session.request_reservation({'reservation_name' : 'res-01', 'duration' : 100})
        >>> print(r.id)
        623
        """
        self.logger.debug('Requesting a reservation using template: {}'.format(template))
        drmaa2_lib = self.get_drmaa2_library()
        template = ReservationTemplate.create_from_dict(template)
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ctypes_reservation = drmaa2_lib.drmaa2_rsession_request_reservation_as(auth._struct, self._struct, template._struct)
        else:
            ctypes_reservation = drmaa2_lib.drmaa2_rsession_request_reservation(self._struct, template._struct)
        if not ctypes_reservation:
            self.exception_mapper.check_last_error_code()
        py_reservation = Reservation(ctypes_reservation)
        self.logger.debug('Got reservation {}'.format(py_reservation))
        drmaa2_lib.drmaa2_r_free(pointer(ctypes_reservation))
        return py_reservation

    def get_reservation(self, id):
        """ 
        Get reservation. 

        :param id: Reservation id.
        :type id: str

        :returns: Reservation object.

        >>> r = r_session.get_reservation('623')
        >>> print(r.id)
        623
        """
        self.logger.debug('Requesting reservation id: {}'.format(id))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_reservation = drmaa2_lib.drmaa2_rsession_get_reservation(self._struct, ByteString(id).encode())
        if not ctypes_reservation:
            self.exception_mapper.check_last_error_code()
        py_reservation = Reservation(ctypes_reservation)
        self.logger.debug('Got reservation {}'.format(py_reservation))
        drmaa2_lib.drmaa2_r_free(pointer(ctypes_reservation))
        return py_reservation

    def get_reservations(self):
        """ 
        Get all reservations. 

        :returns: List of Reservation objects.

        >>> r_list = r_session.get_reservations()
        """
        self.logger.debug('Requesting all reservations')
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_reservation_list = drmaa2_lib.drmaa2_rsession_get_reservations(self._struct)
        if not ctypes_reservation_list:
            self.exception_mapper.check_last_error_code()
        py_reservation_list = Reservation.to_py_reservation_list(ctypes_reservation_list)
        self.logger.debug('Retrieved {} reservations'.format(len(py_reservation_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_reservation_list)))
        return py_reservation_list

