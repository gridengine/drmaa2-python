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
from ctypes import pointer
from ctypes import POINTER

from .drmaa2_constants import Bool
from .drmaa2_constants import Time
from .drmaa2_constants import JobState
from .drmaa2_constants import ListType
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_j
from .drmaa2_ctypes import drmaa2_list_entryfree

from .sudo import Sudo

from .byte_string import ByteString
from .job_info import JobInfo
from .job_template import JobTemplate
from .drmaa2_object import Drmaa2Object
from .log_manager import LogManager
from .exception_mapper import ExceptionMapper
from .drmaa2_exceptions import InvalidArgument


class Job(Drmaa2Object):
    """ High-level DRMAA2 job class. """

    id = Drmaa2Object.StringDescriptor('id')
    """ Job id (str). """
    session_name = Drmaa2Object.StringDescriptor('session_name')
    """ Session name (str). """
    job_name = Drmaa2Object.StringDescriptor('job_name')
    """ Job name (str). """

    logger = LogManager.get_instance().get_logger('Job')

    def __init__(self, job):
        """ Constructor. """
        Drmaa2Object.__init__(self)
        if isinstance(job, POINTER(drmaa2_j)):
            self._struct = POINTER(drmaa2_j)()
            self._struct.contents = drmaa2_j()
            self.id = ByteString(getattr(job.contents, 'id').value).decode()
            self.session_name = ByteString(getattr(job.contents, 'session_name').value).decode()
            self.job_name = ByteString(getattr(job.contents, 'job_name').value).decode()
        else:
            raise InvalidArgument('Invalid argument: %s' % str(job))

    def suspend(self, auth=None):
        """ 
        Suspend the job.

        :param auth: Optional sudo object for suspending the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.suspend()
        >>> print(j.get_info().job_state)
        SUSPENDED
        """
        self.logger.debug('Suspending job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_suspend_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_suspend(self._struct))

    def resume(self, auth=None):
        """ 
        Resume the job.

        :param auth: Optional sudo object for resuming the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.suspend()
        >>> ...
        >>> j.resume()
        """
        self.logger.debug('Resuming job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_resume_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_resume(self._struct))

    def hold(self, auth=None):
        """ 
        Hold the job.

        :param auth: Optional sudo object for holding the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.hold()
        >>> print(j.get_info().job_state)
        RUNNING_HELD
        """
        self.logger.debug('Holding job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_hold_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_hold(self._struct))

    def release(self, auth=None):
        """ 
        Release the job.

        :param auth: Optional sudo object for releasing the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.hold()
        >>> ...
        >>> j.release()
        """
        self.logger.debug('Releasing job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_release_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_release(self._struct))

    def terminate(self, auth=None):
        """ 
        Terminate the job.

        :param auth: Optional sudo object for terminating the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> j.terminate()
        >>> j.get_info().terminating_signal
        'SIGKILL'
        """
        self.logger.debug('Terminating job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            forced = Bool.FALSE
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_as(auth._struct, self._struct, forced))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate(self._struct))

    def terminate_forced(self, auth=None):
        """ 
        Terminate the job (forced).

        :param auth: Optional sudo object for terminating the job; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> j.terminate_forced()
        """
        self.logger.debug('Terminating (forced) job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            forced = Bool.TRUE
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_as(auth._struct, self._struct, forced))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_forced(self._struct))

    def terminate_all(self, auth=None):
        """ 
        Terminate all job tasks.

        :param auth: Optional sudo object for terminating tasks; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.terminate_all()
        """
        self.logger.debug('Terminating all tasks for job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            forced = Bool.FALSE
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_all_as(auth._struct, self._struct, forced))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_all(self._struct))

    def terminate_forced_all(self, auth=None):
        """ 
        Terminate all job tasks (forced).

        :param auth: Optional sudo object for terminating tasks; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> j.terminate_forced_all()
        """
        self.logger.debug('Terminating all tasks (forced) for job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            forced = Bool.TRUE
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_all_as(auth._struct, self._struct, forced))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_terminate_forced_all(self._struct))

    def reap(self):
        """ 
        Reap the job from internal lists.

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> j.reap()
        """
        self.logger.debug('Reaping job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_reap(self._struct))

    def get_template(self):
        """ 
        Get job template.

        :returns: JobTemplate object.

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> jt = j.get_template()
        >>> print(jt.remote_command)
        /bin/sleep
        >>> print(jt.args)
        ['100']
        """
        self.logger.debug('Retrieving template for job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_template = drmaa2_lib.drmaa2_j_get_jtemplate(self._struct)
        if not ctypes_job_template:
            ExceptionMapper.check_last_error_code()

        return JobTemplate(ctypes_job_template)

    def get_state(self):
        """ 
        Get job state.

        :returns: (JobState object, sub-state string) tuple.

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> state,substate = j.get_state()
        >>> print(state)
        JobState.DONE
        """
        self.logger.debug('Retrieving state for job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        sub_state = POINTER(drmaa2_string)()
        sub_state.contents = drmaa2_string()
        jstate = drmaa2_lib.drmaa2_j_get_state(self._struct, sub_state)
        if jstate == int(JobState.UNSET_JSTATE):
            ExceptionMapper.check_last_error_code()
        return (JobState(jstate), sub_state.contents.value)

    def get_info(self):
        """ 
        Get job info.

        :returns: JobInfo object.

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> ...
        >>> ji = j.get_info()
        >>> print(ji.job_id)
        724.1
        >>> print(ji.slots)
        1
        """
        self.logger.debug('Retrieving info for job id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_info = drmaa2_lib.drmaa2_j_get_info(self._struct)
        if not ctypes_job_info:
            ExceptionMapper.check_last_error_code()
        return JobInfo(ctypes_job_info)

    def wait_started(self, timeout=Time.INFINITE_TIME):
        """ 
        Wait until the job starts or specified timeout occurs. 

        :param timeout: Wait timeout in seconds (default: infinite time).
        :type timeout: int

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.wait_started()
        >>> print(j.get_state())
        (<JobState.RUNNING: 3>, None)
        """
        drmaa2_lib = self.get_drmaa2_library()
        self.logger.debug('Waiting on job id {} start'.format(self.id))
        ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_wait_started(self._struct, timeout))

    def wait_terminated(self, timeout=Time.INFINITE_TIME):
        """ 
        Wait until the job terminates or specified timeout occurs.

        :param timeout: Wait timeout in seconds (default: infinite time).
        :type timeout: int

        >>> j = j_session.run_job({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> j.wait_terminated()
        >>> print(j.get_state())
        (<JobState.DONE: 3>, None)
        """
        self.logger.debug('Waiting on job id {} termination'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_j_wait_terminated(self._struct, int(timeout)))

    def __del__(self):
        pass

    @classmethod
    def to_py_job_list(cls, ctypes_list):
        drmaa2_lib = cls.get_drmaa2_library()
        py_job_list = list()
        if ctypes_list:
            count = drmaa2_lib.drmaa2_list_size(ctypes_list)
            cls.logger.debug('Converting ctypes job list of size {}'.format(count))
            for i in range(count):
                void_ptr = drmaa2_lib.drmaa2_list_get(ctypes_list, i)
                if void_ptr:
                    j = cast(void_ptr, POINTER(drmaa2_j))
                    j = Job(j)
                    py_job_list.append(j)
                else:
                    ExceptionMapper.check_last_error_code()
                    py_job_list.append(None)
        return py_job_list

    @classmethod
    def to_ctypes_job_list(cls, py_job_list):
        drmaa2_lib = cls.get_drmaa2_library()
        cls.logger.debug('Converting py job list of size {}'.format(len(py_job_list)))
        ctypes_job_list = drmaa2_lib.drmaa2_list_create(int(ListType.JOBLIST), drmaa2_list_entryfree())
        for j in py_job_list:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_list_add(ctypes_job_list, j._struct))
        return ctypes_job_list
