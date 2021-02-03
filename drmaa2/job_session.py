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

import getpass
from uuid import uuid4
from ctypes import pointer
from ctypes import c_void_p
from .drmaa2_constants import Time
from .drmaa2_constants import PY_DICT_TYPE

from .byte_string import ByteString
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_object import Drmaa2Object

from .sudo import Sudo
from .job_template import JobTemplate
from .job import Job
from .job_info import JobInfo
from .job_array import JobArray
from .log_manager import LogManager
from .exception_mapper import ExceptionMapper
from .drmaa2_exceptions import Drmaa2Exception
from .drmaa2_exceptions import InvalidArgument


class JobSession(Drmaa2Object):
    """ High-level DRMAA2 job session class. """

    name = Drmaa2Object.StringDescriptor('name')
    """ Job session name (str). """
    contact = Drmaa2Object.StringDescriptor('contact')
    """ Job session contact (str). """

    logger = LogManager.get_instance().get_logger('JobSession')
    exception_mapper = ExceptionMapper()

    def __init__(self, name=None, contact=None, destroy_on_exit=True, check_for_existing_session=True, session_dict={},
                 auth=None):
        """ 
        Constructor. If the session with a given name does not already exist, 
        it will create a new one; otherwise, it will open the existing session.

        :param name: Session name; it may be also be specified as part of the job session object dictionary. If not provided, a random name will be used.
        :type name: str

        :param contact: Session contact; it may be also be specified as part of the job session object dictionary.
        :type contact: str

        :param destroy_on_exit: Destroy session when the job session object goes out of scope.
        :type destroy_on_exit: bool

        :param check_for_existing_session: If false, the constructor will not check for existing session with the given name.
        :type check_for_existing_session: bool

        :param session_dict: Job session dictionary; if specified, it should contain 'name' and (optionally) 'contact' keys.
        :type session_dict: dict

        :param auth: Optional sudo object for creating the session; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j_session = JobSession()
        >>> print(j_session.name)
        bab80df52a654dfda7552cbae8dacca
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
                session_names_to_check.append('%s@%s' % (contact, name))
            else:
                session_names_to_check.append('%s@%s' % (getpass.getuser(), name))
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

        :returns: List of existing job session names.

        >>> print(JobSession.list_session_names())
        ['auser@js-01']
        """
        return Drmaa2Object.to_py_string_list(cls.get_drmaa2_library().drmaa2_get_jsession_names())

    def __create(self, name, contact, auth):
        self.logger.debug('Creating job session with name {} (contact: {})'.format(name, contact))
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            struct = self.get_drmaa2_library().drmaa2_create_jsession_as(auth._struct, ByteString(name).encode(),
                                                                         ByteString(contact).encode())
        else:
            if '@' in name:
                raise InvalidArgument('session name with @ is not allowed')
            struct = self.get_drmaa2_library().drmaa2_create_jsession(ByteString(name).encode(),
                                                                      ByteString(contact).encode())
        if not struct:
            self.exception_mapper.check_last_error_code()
        return struct

    def __open(self, name):
        self.logger.debug('Opening job session {}'.format(name))
        struct = self.get_drmaa2_library().drmaa2_open_jsession(ByteString(name).encode())
        if not struct:
            self.exception_mapper.check_last_error_code()
        return struct

    def open(self):
        """ 
        Open session. This method is called automatically in the constructor.

        >>> ...
        >>> j_session.close()
        >>> ...
        >>> j_session.open()
        """
        if self._struct:
            self.logger.debug('Job session {} is already open'.format(self._name_bs.decode()))
        else:
            self._struct = self.__open(self._name_bs)
            self._struct_p = pointer(self._struct)

    def close(self):
        """ 
        Close session. This method is called automatically when the session
        object goes out of scope.

        >>> ...
        >>> j_session.close()
        """
        if self._struct:
            self.logger.debug('Closing job session {}'.format(self._name_bs.decode()))
            drmaa2_lib = self.get_drmaa2_library()
            self.exception_mapper.check_status_code(drmaa2_lib.drmaa2_close_jsession(self._struct))
            drmaa2_lib.drmaa2_jsession_free(self._struct_p)
            self._struct = None

    def destroy(self, auth=None):
        """ 
        Destroy session. This method is called automatically when the 
        session object goes out of scope, unless the destroy_on_exit flag is set to false.

        :param auth: Optional sudo object for destroying the session; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ...
        >>> j_session.destroy()
        """
        self.logger.debug('Destroying job session {}'.format(self._name_bs.decode()))
        auth = auth or self._auth
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            if self._name_bs.decode() != ByteString('').decode():
                self.exception_mapper.check_status_code(
                    self.get_drmaa2_library().drmaa2_destroy_jsession_as(auth._struct, self._name_bs.encode()))
        else:
            if self._name_bs.decode() != ByteString('').decode():
                self.exception_mapper.check_status_code(
                    self.get_drmaa2_library().drmaa2_destroy_jsession(self._name_bs.encode()))

    @classmethod
    def destroy_by_name(cls, name, auth=None):
        """ 
        Destroy session by name. 

        :param name: Session name.
        :type name: str

        :param auth: Optional sudo object for destroying the session; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> JobSession.destroy_by_name('js-01')
        """
        cls.logger.debug('Destroying job session {}'.format(name))
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            cls.exception_mapper.check_status_code(
                cls.get_drmaa2_library().drmaa2_destroy_jsession_as(auth._struct, ByteString(name).encode()))
        else:
            cls.exception_mapper.check_status_code(
                cls.get_drmaa2_library().drmaa2_destroy_jsession(ByteString(name).encode()))

    def __del__(self):
        """ Destructor. """
        self.close()
        if self._destroy_on_exit:
            try:
                self.destroy()
            except Drmaa2Exception as ex:
                self.logger.warn('Could not destroy job session: {}'.format(str(ex)))
        else:
            self.logger.debug('Will not destroy job session {}'.format(self._name_bs.decode()))
        if self._struct:
            self.get_drmaa2_library().drmaa2_jsession_free(self._struct_p)

    def run_job(self, template, auth=None):
        """ 
        Run a job using template. 

        :param template: Job template; it can be specified either as a dictionary, or directly as a JobTemplate object.
        :type template: JobTemplate or dict

        :param auth: Optional sudo object for running the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        :returns: Job object.

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['10']})
        >>> print(j)
        {'id': '521', 'session_name': 'js-01'}
        >>> type(j)
        <class 'drmaa2.job.Job'>
        >>> print(j.id)
        521
        """
        self.logger.debug('Running a job using template: {}'.format(template))
        drmaa2_lib = self.get_drmaa2_library()
        template = JobTemplate.create_from_dict(template)
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ctypes_job = drmaa2_lib.drmaa2_jsession_run_job_as(auth._struct, self._struct, template._struct)
        else:
            ctypes_job = drmaa2_lib.drmaa2_jsession_run_job(self._struct, template._struct)
        if not ctypes_job:
            self.exception_mapper.check_last_error_code()
        py_job = Job(ctypes_job)
        self.logger.debug('Got job {}'.format(py_job))
        drmaa2_lib.drmaa2_j_free(pointer(ctypes_job))
        return py_job

    def run_bulk_jobs(self, template, begin_index, end_index, step, max_parallel, auth=None):
        """ 
        Run an array job using template. 

        :param template: Job template; it can be specified either as a dictionary, or directly as a JobTemplate object.
        :type template: JobTemplate or dict

        :param begin_index: Begin index.
        :type begin_index: long

        :param end_index: End index.
        :type end_index: long

        :param step: Index step. 
        :type step: long

        :param max_parallel: Max. number of parallel tasks.
        :type max_parallel: long

        :param auth: Optional sudo object for running the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        :returns: JobArray object.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> print(ja)
        {'id': '528', 'job_list': [Job({'id': '528.1', 'session_name': 'js-01'}), Job({'id': '528.4', 'session_name': 'js-01'}), Job({'id': '528.7', 'session_name': 'js-01'}), Job({'id': '528.10', 'session_name': 'js-01'})], 'session_name': 'js-01'}
        >>> type(ja)
        <class 'drmaa2.job_array.JobArray'>
        """
        self.logger.debug(
            'Running an array job with task indices ({},{},{}), max. parallel {}, and using template: {}'.format(
                begin_index, end_index, step, max_parallel, template))
        drmaa2_lib = self.get_drmaa2_library()
        template = JobTemplate.create_from_dict(template)

        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ctypes_job_array = drmaa2_lib.drmaa2_jsession_run_bulk_jobs_as(auth._struct, self._struct, template._struct,
                                                                           begin_index, end_index, step, max_parallel)
        else:
            ctypes_job_array = drmaa2_lib.drmaa2_jsession_run_bulk_jobs(self._struct, template._struct, begin_index,
                                                                        end_index, step, max_parallel)
        if not ctypes_job_array:
            self.exception_mapper.check_last_error_code()
        py_job_array = JobArray(ctypes_job_array)
        self.logger.debug('Got job array {}'.format(py_job_array))
        return py_job_array

    def wait_any_started(self, job_list, timeout=Time.INFINITE_TIME):
        """ 
        Wait for start of any job from the given list . 

        :param job_list: Job list.
        :type job_list: [Job]

        :param timeout: Wait timeout in seconds (default: infinite time).
        :type timeout: int

        :returns: Started Job object.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> print(ja)
        {'id': '542', 'job_list': [Job({'id': '542.1', 'session_name': 'js-01'}), Job({'id': '542.4', 'session_name': 'js-01'}), Job({'id': '542.7', 'session_name': 'js-01'}), Job({'id': '542.10', 'session_name': 'js-01'})], 'session_name': 'js-01'}
        >>> j = j_session.wait_any_started(ja.job_list)
        >>> print(j)
        {'id': '542.1', 'session_name': 'js-01'}
        """
        self.logger.debug('Wating for any one of {} jobs to start'.format(len(job_list)))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_list = Job.to_ctypes_job_list(job_list)
        ctypes_job = drmaa2_lib.drmaa2_jsession_wait_any_started(self._struct, ctypes_job_list, int(timeout))
        if not ctypes_job:
            self.exception_mapper.check_last_error_code()
        py_job = Job(ctypes_job)
        self.logger.debug('Job {} started'.format(py_job))
        drmaa2_lib.drmaa2_j_free(pointer(ctypes_job))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list)))
        return py_job

    def wait_any_terminated(self, job_list, timeout=Time.INFINITE_TIME):
        """ 
        Wait for termination of any job from the given list . 

        :param job_list: Job list.
        :type job_list: [Job]

        :param timeout: Wait timeout in seconds (default: infinite time).
        :type timeout: int

        :returns: Terminated Job object.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> print(ja)
        {'id': '542', 'job_list': [Job({'id': '542.1', 'session_name': 'js-01'}), Job({'id': '542.4', 'session_name': 'js-01'}), Job({'id': '542.7', 'session_name': 'js-01'}), Job({'id': '542.10', 'session_name': 'js-01'})], 'session_name': 'js-01'}
        >>> j = j_session.wait_any_terminated(ja.job_list)
        >>> print(j)
        {'id': '542.1', 'session_name': 'js-01'}
        """
        self.logger.debug('Wating for any one of {} jobs to terminate'.format(len(job_list)))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_list = Job.to_ctypes_job_list(job_list)
        ctypes_job = drmaa2_lib.drmaa2_jsession_wait_any_terminated(self._struct, ctypes_job_list, int(timeout))
        if not ctypes_job:
            self.exception_mapper.check_last_error_code()
        py_job = Job(ctypes_job)
        self.logger.debug('Job {} terminated'.format(py_job))
        drmaa2_lib.drmaa2_j_free(pointer(ctypes_job))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list)))
        return py_job

    def wait_all_started(self, job_list, timeout=Time.INFINITE_TIME):
        """ 
        Wait for start of all jobs from the given list . 

        :param job_list: Job list.
        :type job_list: [Job]

        :param timeout: Wait timeout in seconds (default: infinite time).
        :type timeout: int

        :returns: List of started Job objects.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> print(ja)
        {'id': '542', 'job_list': [Job({'id': '542.1', 'session_name': 'js-01'}), Job({'id': '542.4', 'session_name': 'js-01'}), Job({'id': '542.7', 'session_name': 'js-01'}), Job({'id': '542.10', 'session_name': 'js-01'})], 'session_name': 'js-01'}
        >>> jl = js.wait_all_started(ja.job_list)
        >>> print(jl)
        [Job({'id': '542.1', 'session_name': 'js-01'}), Job({'id': '542.4', 'session_name': 'js-01'}), Job({'id': '542.7', 'session_name': 'js-01'}), Job({'id': '542.10', 'session_name': 'js-01'})]
        """
        self.logger.debug('Wating for all of {} jobs to start'.format(len(job_list)))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_list = Job.to_ctypes_job_list(job_list)
        ctypes_job_list2 = drmaa2_lib.drmaa2_jsession_wait_all_started(self._struct, ctypes_job_list, int(timeout))
        if not ctypes_job_list2:
            self.exception_mapper.check_last_error_code()
        py_job_list = Job.to_py_job_list(ctypes_job_list2)
        self.logger.debug('All {} jobs started'.format(len(job_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list2)))
        return py_job_list

    def wait_all_terminated(self, job_list, timeout=Time.INFINITE_TIME):
        """ 
        Wait for termination of all jobs from the given list . 

        :param job_list: Job list.
        :type job_list: [Job]

        :param timeout: Wait timeout in seconds (default: infinite time).
        :type timeout: int

        :returns: List of terminated Job objects.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> print(ja)
        {'id': '542', 'job_list': [Job({'id': '542.1', 'session_name': 'js-01'}), Job({'id': '542.4', 'session_name': 'js-01'}), Job({'id': '542.7', 'session_name': 'js-01'}), Job({'id': '542.10', 'session_name': 'js-01'})], 'session_name': 'js-01'}
        >>> jl = js.wait_all_terminated(ja.job_list)
        >>> print(jl)
        [Job({'id': '542.1', 'session_name': 'js-01'}), Job({'id': '542.4', 'session_name': 'js-01'}), Job({'id': '542.7', 'session_name': 'js-01'}), Job({'id': '542.10', 'session_name': 'js-01'})]
        """
        self.logger.debug('Wating for all of {} jobs to terminate'.format(len(job_list)))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_list = Job.to_ctypes_job_list(job_list)
        ctypes_job_list2 = drmaa2_lib.drmaa2_jsession_wait_all_terminated(self._struct, ctypes_job_list, int(timeout))
        if not ctypes_job_list2:
            self.exception_mapper.check_last_error_code()
        py_job_list = Job.to_py_job_list(ctypes_job_list2)
        self.logger.debug('All {} jobs terminated'.format(len(job_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list)))
        drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list2)))
        return py_job_list

    def get_job_array(self, id):
        """ 
        Get job array.

        :param id: Job array id.
        :type id: str

        :returns: Job array object.

        >>> ja = j_session.get_job_array(ja_id)
        """
        self.logger.debug('Retrieving job array id {}'.format(id))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_array = drmaa2_lib.drmaa2_jsession_get_job_array(self._struct, ByteString(id).encode())
        if not ctypes_job_array:
            self.exception_mapper.check_last_error_code()
        py_job_array = JobArray(ctypes_job_array)
        self.logger.debug('Got job array {}'.format(py_job_array))
        return py_job_array

    def get_job_categories(self):
        """ 
        Get list of all job categories.

        :returns: List of job categories

        >>> j_session = JobSession('js-01')
        >>> print(j_session.get_job_categories())
        []
        """
        drmaa2_lib = self.get_drmaa2_library()
        return Drmaa2Object.to_py_string_list(drmaa2_lib.drmaa2_jsession_get_job_categories(self._struct))

    def get_jobs(self, filter):
        """ 
        Get jobs matching the specified info.

        :param filter: Job info filter.
        :type filter: JobInfo

        :returns: List of Job objects.

        >>> j_info = JobInfo({'job_name' : 'a_job'})
        >>> j_list = j_session.get_all_jobs(j_info)
        """
        self.logger.debug('Requesting list of jobs using filter: {}'.format(filter))
        drmaa2_lib = self.get_drmaa2_library()
        job_info = filter
        if type(filter) == PY_DICT_TYPE:
            job_info = JobInfo(filter)
        ctypes_filter = job_info._struct
        ctypes_job_list = drmaa2_lib.drmaa2_jsession_get_jobs(self._struct, ctypes_filter)
        if not ctypes_job_list:
            self.exception_mapper.check_last_error_code()

        py_job_list = []
        if ctypes_job_list:
            py_job_list = Job.to_py_job_list(ctypes_job_list)
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_job_list)))
        return py_job_list
