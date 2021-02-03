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

from ctypes import POINTER
from ctypes import pointer

from .drmaa2_constants import *
from .drmaa2_ctypes import drmaa2_jinfo
from .drmaa2_object import Drmaa2Object
# from .drmaa2_slot_info_list_descriptor import Drmaa2SlotInfoListDescriptor
from .drmaa2_exceptions import InvalidArgument


class JobInfo(Drmaa2Object):
    """ High-level DRMAA2 job info class. """

    job_id = Drmaa2Object.StringDescriptor('jobId')
    """ Job id (str). """
    job_name = Drmaa2Object.StringDescriptor('jobName')
    """ Job name (str). """
    exit_status = Drmaa2Object.IntDescriptor('exitStatus')
    """ Job exit status (int). """
    terminating_signal = Drmaa2Object.StringDescriptor('terminatingSignal')
    """ Job terminating signal (str). """
    annotation = Drmaa2Object.StringDescriptor('annotation')
    """ Annotation (str). """
    job_state = Drmaa2Object.EnumDescriptor('jobState', JobState)
    """ Job state (JobState). """
    job_sub_state = Drmaa2Object.StringDescriptor('jobSubState')
    """ Job sub state (str). """
    allocated_machines = Drmaa2Object.StringListDescriptor('allocatedMachines')
    # allocated_machines = Drmaa2SlotInfoListDescriptor('allocatedMachines')
    """ List of machines allocated to the job ([str]). """
    submission_machine = Drmaa2Object.StringDescriptor('submissionMachine')
    """ Job submission machine (str). """
    job_owner = Drmaa2Object.StringDescriptor('jobOwner')
    """ Job owner (str). """
    slots = Drmaa2Object.LongLongDescriptor('slots')
    """ Number of job slots (long). """
    queue_name = Drmaa2Object.StringDescriptor('queueName')
    """ Queue name (str). """
    wallclock_time = Drmaa2Object.TimeDescriptor('wallclockTime')
    """ Wallclock time (long). """
    cpu_time = Drmaa2Object.LongLongDescriptor('cpuTime')
    """ CPU time (long). """
    submission_time = Drmaa2Object.TimeDescriptor('submissionTime')
    """ Submission time (datetime). """
    dispatch_time = Drmaa2Object.TimeDescriptor('dispatchTime')
    """ Dispatch time (datetime). """
    finish_time = Drmaa2Object.TimeDescriptor('finishTime')
    """ Finish time (datetime). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, job_info={}):
        """ 
        Constructor. 

        :param job_info: Input structure representing the object; this structure is typically a dictionary, but it can also be a low-level drmaa2_jinfo struct.
        :type job_info: dict 

        :raises InvalidArgument: in case of an invalid input argument.
        :raises Drmaa2Exception: for all other errors.

        >>> ji = JobInfo({'queue_name' : 'all.q', 'job_owner' : 'auser'})
        >>> print(ji.queue_name)
        all.q
        >>> ji.slots = 2
        >>> print(ji.slots)
        2
        """
        Drmaa2Object.__init__(self)
        if isinstance(job_info, dict):
            self._struct = POINTER(drmaa2_jinfo)()
            self._struct.contents = drmaa2_jinfo()
            # self._struct = self.get_drmaa2_library().drmaa2_jinfo_create()
            self.__init_defaults()
            self.init_impl_spec_key_values()
            self.from_dict(job_info)
        elif isinstance(job_info, POINTER(drmaa2_jinfo)):
            self._struct = job_info
        else:
            raise InvalidArgument('Invalid argument: %s' % str(job_info))

    def __del__(self):
        # self.get_drmaa2_library().drmaa2_jinfo_free(pointer(self._struct))
        pass

    def __init_defaults(self):
        self.job_id = None
        self.wallclock_time = UNSET_TIME
        self.exit_status = UNSET_NUM
        self.finish_time = UNSET_TIME
        self.job_state = JobState.UNSET_JSTATE
        self.submission_time = UNSET_TIME
        self.slots = UNSET_NUM
        self.dispatch_time = UNSET_TIME
        self.cpu_time = UNSET_NUM
        self.allocated_machines = None

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.

        >>> print(JobInfo.get_implementation_specific_keys())
        ['uge_ji_priority', 'uge_ji_failed', 'uge_ji_mem', 'uge_ji_rss', 'uge_ji_vmem']
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(cls.get_drmaa2_library().drmaa2_jinfo_impl_spec())
        return cls.implementation_specific_keys
