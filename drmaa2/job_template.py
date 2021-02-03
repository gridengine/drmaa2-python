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

from .drmaa2_constants import UNSET_PRIORITY
from .drmaa2_constants import Os
from .drmaa2_constants import Cpu
from .drmaa2_ctypes import drmaa2_jtemplate
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_object import Drmaa2Object
from .drmaa2_exceptions import InvalidArgument


class JobTemplate(Drmaa2Object):
    """ High-level DRMAA2 job template class. """

    remote_command = Drmaa2Object.StringDescriptor('remoteCommand')
    """ Job executable (str). """
    args = Drmaa2Object.StringListDescriptor('args')
    """ Arguments for the job executable ([str]). """
    submit_as_hold = Drmaa2Object.BoolDescriptor('submitAsHold')
    """ Submit as hold flag (bool). """
    rerunnable = Drmaa2Object.BoolDescriptor('rerunnable')
    """ Rerrunable flag (bool). """
    job_environment = Drmaa2Object.DictDescriptor('jobEnvironment')
    """ Job environment variables (dictionary). """
    working_directory = Drmaa2Object.StringDescriptor('workingDirectory')
    """ Working directory (str). """
    job_category = Drmaa2Object.StringDescriptor('jobCategory')
    """ Job category (str). """
    email = Drmaa2Object.StringListDescriptor('email')
    """ List of emails for notifications ([str]). """
    email_on_started = Drmaa2Object.BoolDescriptor('emailOnStarted')
    """ Email on started flag (bool). """
    email_on_terminated = Drmaa2Object.BoolDescriptor('emailOnTerminated')
    """ Email on terminated flag (bool). """
    job_name = Drmaa2Object.StringDescriptor('jobName')
    """ Job name (str). """
    input_path = Drmaa2Object.StringDescriptor('inputPath')
    """ Input file path (str). """
    output_path = Drmaa2Object.StringDescriptor('outputPath')
    """ Output file path (str). """
    error_path = Drmaa2Object.StringDescriptor('errorPath')
    """ Error file path (str). """
    join_files = Drmaa2Object.BoolDescriptor('joinFiles')
    """ Join files flag (bool). """
    reservation_id = Drmaa2Object.StringDescriptor('reservationId')
    """ Reservation id (str). """
    queue_name = Drmaa2Object.StringDescriptor('queueName')
    """ Requested queue (str). """
    min_slots = Drmaa2Object.LongLongDescriptor('minSlots')
    """ Minimum number of slots required by the job (long). """
    max_slots = Drmaa2Object.LongLongDescriptor('maxSlots')
    """ Maximum number of slots required by the job (long). """
    priority = Drmaa2Object.LongLongDescriptor('priority', unset_value=UNSET_PRIORITY)
    """ Job priority (long). """
    candidate_machines = Drmaa2Object.StringListDescriptor('candidateMachines')
    """ List of machines that are candidate for running the job ([str]). """
    min_phys_memory = Drmaa2Object.LongLongDescriptor('minPhysMemory')
    """ Minimum physical memory needed for the job (long). """
    machine_os = Drmaa2Object.EnumDescriptor('machineOS', Os)
    """ OS required for the job (Os). """
    machine_arch = Drmaa2Object.EnumDescriptor('machineArch', Cpu)
    """ Machine arch required for the job (Cpu). """
    start_time = Drmaa2Object.TimeDescriptor('startTime')
    """ Requested start time (datetime). """
    deadline_time = Drmaa2Object.TimeDescriptor('deadlineTime')
    """ Deadline time (datetime). """
    stage_in_files = Drmaa2Object.DictDescriptor('stageInFiles')
    """ Stage in files ({str:str}). """
    stage_out_files = Drmaa2Object.DictDescriptor('stageOutFiles')
    """ Stage out files ({str:str}). """
    resource_limits = Drmaa2Object.DictDescriptor('resourceLimits')
    """ Resource limits ({str:str}). """
    accounting_id = Drmaa2Object.StringDescriptor('accountingId')
    """ Accounting id (str). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, template={}):
        """ 
        Constructor. 

        :param template: Input structure representing the object; this structure is typically a dictionary, but it can also be a low-level drmaa2_jtemplate struct.
        :type template: dict 

        :raises InvalidArgument: in case of an invalid input argument.
        :raises Drmaa2Exception: for all other errors.

        >>> jt = JobTemplate({'remote_command' : '/bin/sleep', 'args' : ['100']})
        >>> print(jt.remote_command)
        /bin/sleep
        >>> jt.rerunnable = True
        >>> print(jt.get_implementation_specific_keys())
        ['uge_jt_pe', 'uge_jt_native']
        """
        Drmaa2Object.__init__(self)
        if isinstance(template, dict):
            self._struct = self.get_drmaa2_library().drmaa2_jtemplate_create()
            # self._struct = POINTER(drmaa2_jtemplate)
            # self._struct.contents = drmaa2_jtemplate()
            self.init_impl_spec_key_values()
            self.from_dict(template)
        elif isinstance(template, POINTER(drmaa2_jtemplate)):
            self._struct = template
        else:
            raise InvalidArgument('Invalid argument: %s' % str(template))

    def __del__(self):
        setattr(self._struct.contents, 'remoteCommand', drmaa2_string())
        setattr(self._struct.contents, 'workingDirectory', drmaa2_string())
        setattr(self._struct.contents, 'jobCategory', drmaa2_string())
        setattr(self._struct.contents, 'jobName', drmaa2_string())
        setattr(self._struct.contents, 'inputPath', drmaa2_string())
        setattr(self._struct.contents, 'outputPath', drmaa2_string())
        setattr(self._struct.contents, 'errorPath', drmaa2_string())
        setattr(self._struct.contents, 'reservationId', drmaa2_string())
        setattr(self._struct.contents, 'queueName', drmaa2_string())
        setattr(self._struct.contents, 'job_environment', dict())
        setattr(self._struct.contents, 'stage_in_files', dict())
        setattr(self._struct.contents, 'stage_out_files', dict())
        setattr(self._struct.contents, 'resource_limits', dict())
        setattr(self._struct.contents, 'accountingId', drmaa2_string())
        self.get_drmaa2_library().drmaa2_jtemplate_free(pointer(self._struct))

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(
                cls.get_drmaa2_library().drmaa2_jtemplate_impl_spec())
        return cls.implementation_specific_keys
