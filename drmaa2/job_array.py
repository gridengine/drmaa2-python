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

from ctypes import pointer
from ctypes import POINTER

from .drmaa2_constants import Bool
from .drmaa2_constants import Time
from .drmaa2_constants import JobState
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_jarray

from .sudo import Sudo

from .byte_string import ByteString
from .job import Job
from .job_info import JobInfo
from .job_template import JobTemplate
from .drmaa2_object import Drmaa2Object
from .log_manager import LogManager
from .exception_mapper import ExceptionMapper
from .drmaa2_job_list_descriptor import Drmaa2JobListDescriptor


class JobArray(Drmaa2Object):
    """ High-level DRMAA2 job array class. """

    id = Drmaa2Object.StringDescriptor('id')
    """ Job id (str). """
    session_name = Drmaa2Object.StringDescriptor('session_name')
    """ Session name (str). """
    job_list = Drmaa2JobListDescriptor('job_list')
    """ Job list ([Job]). """

    logger = LogManager.get_instance().get_logger('Job')

    def __init__(self, struct=None):
        """ Constructor. """
        Drmaa2Object.__init__(self, struct)

    def suspend(self, auth=None):
        """ 
        Suspend the job array.

        :param auth: Optional sudo object for suspending the job array; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> ...
        >>> ja.suspend()
        """
        self.logger.debug('Suspending job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_suspend_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_suspend(self._struct))

    def resume(self, auth=None):
        """ 
        Resume the job array.

        :param auth: Optional sudo object for resuming the job array; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> ...
        >>> ja.suspend()
        >>> ...
        >>> ja.resume()
        """
        self.logger.debug('Resuming job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_resume_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_resume(self._struct))

    def hold(self, auth=None):
        """ 
        Hold the job array.

        :param auth: Optional sudo object for holding the job array; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> ...
        >>> ja.hold()
        """
        self.logger.debug('Holding job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_hold_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_hold(self._struct))

    def release(self, auth=None):
        """ 
        Release the job array.

        :param auth: Optional sudo object for releasing the job array; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 2)
        >>> ...
        >>> ja.hold()
        >>> ...
        >>> ja.release()
        """
        self.logger.debug('Releasing job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_release_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_release(self._struct))

    def terminate(self, auth=None):
        """ 
        Terminate the job array.

        :param auth: Optional sudo object for terminating the job array; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['100']}, 1, 10, 3, 1)
        >>> ...
        >>> ja.terminate()
        """
        self.logger.debug('Terminating job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_terminate_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_terminate(self._struct))

    def terminate_all(self, auth=None):
        """ 
        Terminate all job array tasks.

        :param auth: Optional sudo object for terminating job array tasks; it can be specified either as a dictionary, or as a Sudo object directly.
        :type auth: Sudo or dict

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['100']}, 1, 10, 3, 3)
        >>> ...
        >>> ja.terminate_all()
        """
        self.logger.debug('Terminating all tasks for job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        if auth:
            auth = Sudo.create_from_dict(auth)
            self.logger.debug('Using sudo object: {}'.format(auth))
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_terminate_all_as(auth._struct, self._struct))
        else:
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_terminate_all(self._struct))

    def reap(self):
        """ 
        Reap the job array from internal lists.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['10']}, 1, 10, 3, 3)
        >>> ...
        >>> ja.reap()
        """
        self.logger.debug('Reaping job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_jarray_reap(self._struct))

    def get_template(self):
        """ 
        Get job array template.

        :returns: JobTemplate object.

        >>> ja = j_session.run_bulk_jobs({'remote_command' : '/bin/sleep', 'args' : ['100']}, 1, 10, 5, 2)
        >>> ...
        >>> jt = ja.get_template()
        >>> print(jt.remote_command)
        /bin/sleep
        >>> print(jt.args)
        ['100']
        """
        self.logger.debug('Retrieving template for job array id {}'.format(self.id))
        drmaa2_lib = self.get_drmaa2_library()
        ctypes_job_template = drmaa2_lib.drmaa2_jarray_get_jtemplate(self._struct)
        if not ctypes_job_template:
            self.exception_mapper.check_last_error_code()

        return JobTemplate(ctypes_job_template)

    def __del__(self):
        if self._struct:
            self.get_drmaa2_library().drmaa2_jarray_free(pointer(self._struct))
