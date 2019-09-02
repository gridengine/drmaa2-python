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

from uuid import uuid4
from ctypes import pointer
from ctypes import c_void_p

from .drmaa2_constants import PY_DICT_TYPE

from .byte_string import ByteString
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_machineinfo_list
from .drmaa2_object import Drmaa2Object

from .machine_info import MachineInfo
from .queue_info import QueueInfo
from .reservation_info import ReservationInfo
from .reservation import Reservation
from .job_info import JobInfo
from .job import Job
from .log_manager import LogManager
from .exception_mapper import ExceptionMapper


class MonitoringSession(Drmaa2Object):
    """ High-level DRMAA2 monitoring session class. """

    name = Drmaa2Object.StringDescriptor('name')
    """ Monitoring session name (str). """

    logger = LogManager.get_instance().get_logger('JobSession')
    exception_mapper = ExceptionMapper()

    def __init__(self, name=None, session_dict={}):
        """ 
        Constructor. If the session with a given name does not already exist, 
        it will create a new one; otherwise, it will open the existing session.

        :param name: Session name; it may be also be specified as part of the monitoring session object dictionary. If not provided, a random name will be used.
        :type name: str

        :param session_dict: Monitoring session dictionary; if specified, it should contain the 'name' key.
        :type session_dict: dict

        >>> m_session = MonitoringSession()
        >>> print(m_session.name)
        b6db641c6bf34ffaafaac15d31554778
        """
        Drmaa2Object.__init__(self)
        name = name or session_dict.get('name')
        if not name:
            name = uuid4().hex
        self._struct = self.__open(name)
        self._struct_p = pointer(self._struct)
        self._name_bs = ByteString(name)
        self._read_only = True

    def __open(self, name):
        self.logger.debug('Opening monitoring session {}'.format(name))
        struct = self.get_drmaa2_library().drmaa2_open_msession(ByteString(name).encode())
        if not struct:
            self.exception_mapper.check_last_error_code()
        return struct

    def open(self):
        """ 
        Open session. This method is called automatically in the constructor.

        >>> ...
        >>> m_session.close()
        >>> ...
        >>> m_session.open()
        >>> mi_list = m_session.get_all_machines(['univa.example.com'])
        """
        if self._struct:
            self.logger.debug('Monitoring session {} is already open'.format(self._name_bs.decode()))
        else:
            self._struct = self.__open(self._name_bs)
            self._struct_p = pointer(self._struct)

    def close(self):
        """ 
        Close session. This method is called automatically when the session
        object goes out of scope.

        >>> mi_list = m_session.get_all_machines(['univa.example.com'])
        >>> m_session.close()
        """
        if self._struct:
            self.logger.debug('Closing monitoring session {}'.format(self._name_bs.decode()))
            drmaa2_lib = self.get_drmaa2_library()
            self.exception_mapper.check_status_code(drmaa2_lib.drmaa2_close_msession(self._struct))
            drmaa2_lib.drmaa2_msession_free(self._struct_p)
            self._struct = None

    def __del__(self):
        """ Destructor. """
        self.close()

    def get_all_machines(self, filter):
        """ 
        Get information about specified machines.

        :param filter: List of machine names to retrieve information for.
        :type filter: [str]

        :returns: List of MachineInfo objects.

        >>> mi_list = m_session.get_all_machines(['univa.example.com'])
        >>> print(mi_list)
         [MachineInfo({'available': 'TRUE', 'cores_per_socket': 1, 'implementation_specific': {}, 'load': 0.07999999821186066, 'machine_arch': 'X64', 'machine_os': 'OTHER_OS', 'machine_os_version': Version({'implementation_specific': {}}), 'name': 'univ.example.com', 'phys_memory': 4047372, 'sockets': 1, 'threads_per_core': 1, 'virt_memory': 8110599})]
        """
        self.logger.debug('Requesting list of machines using filter: {}'.format(filter))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_filter = self.to_ctypes_string_list(filter)
        ctypes_machine_info_list = drmaa2_lib.drmaa2_msession_get_all_machines(self._struct, ctypes_filter)
        if not ctypes_machine_info_list:
            self.exception_mapper.check_last_error_code()

        py_machine_info_list = []
        if ctypes_machine_info_list:
            py_machine_info_list = MachineInfo.to_py_machine_info_list(ctypes_machine_info_list)
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_machine_info_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_filter)))
        return py_machine_info_list

    def get_all_queues(self, filter):
        """ 
        Get information about specified queues.

        :param filter: List of queue names to retrieve information for.
        :type filter: [str]

        :returns: List of QueueInfo objects.

        >>> qi_list = m_session.get_all_queues(['all.q'])
        >>> print(qi_list)
        [QueueInfo({'implementation_specific': {}, 'name': 'all.q'})]
        """
        self.logger.debug('Requesting list of queues using filter: {}'.format(filter))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_filter = self.to_ctypes_string_list(filter)
        ctypes_queue_info_list = drmaa2_lib.drmaa2_msession_get_all_queues(self._struct, ctypes_filter)
        if not ctypes_queue_info_list:
            self.exception_mapper.check_last_error_code()

        py_queue_info_list = []
        if ctypes_queue_info_list:
            py_queue_info_list = QueueInfo.to_py_queue_info_list(ctypes_queue_info_list)
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_queue_info_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_filter)))
        return py_queue_info_list

    def get_all_reservations(self, filter):
        """ 
        Get reservations matching the specified info.

        :param filter: Reservation info filter.
        :type filter: ReservationInfo

        :returns: List of Reservation objects.

        >>> ri = ReservationInfo({'reservation_name' : r_name})
        >>> r_list = m_session.get_all_reservations(ri)
        >>> print(r_list)
        [Reservation({'id': '49'})]
        """
        self.logger.debug('Requesting list of reservations using filter: {}'.format(filter))
        drmaa2_lib = self.get_drmaa2_library()
        reservation_info = filter
        if type(filter) == PY_DICT_TYPE:
            reservation_info = ReservationInfo(filter)
        ctypes_filter = reservation_info._struct
        ctypes_reservation_list = drmaa2_lib.drmaa2_msession_get_all_reservations(self._struct, ctypes_filter)
        if not ctypes_reservation_list:
            self.exception_mapper.check_last_error_code()

        py_reservation_list = []
        if ctypes_reservation_list:
            py_reservation_list = Reservation.to_py_reservation_list(ctypes_reservation_list)
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_reservation_list)))
        return py_reservation_list

    def get_all_jobs(self, filter):
        """ 
        Get jobs matching the specified info.

        :param filter: Job info filter.
        :type filter: JobInfo

        :returns: List of Job objects.

        >>> j_info = JobInfo({'job_name' : 'a_job'})
        >>> j_list = m_session.get_all_jobs(j_info)
        """
        self.logger.debug('Requesting list of jobs using filter: {}'.format(filter))
        drmaa2_lib = self.get_drmaa2_library()
        job_info = filter
        if type(filter) == PY_DICT_TYPE:
            job_info = JobInfo(filter)
        ctypes_filter = job_info._struct
        ctypes_job_list = drmaa2_lib.drmaa2_msession_get_all_jobs(self._struct, ctypes_filter)
        if not ctypes_job_list:
            self.exception_mapper.check_last_error_code()

        py_job_list = []
        if ctypes_job_list:
            py_job_list = Job.to_py_job_list(ctypes_job_list)
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list)))
        return py_job_list
