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

"""
Definitions for DRMAA2 ctypes.
"""

import ctypes
import platform
from ctypes import c_void_p
from ctypes import c_byte
from ctypes import c_char
from ctypes import c_char_p
from ctypes import c_long
from ctypes import c_int
from ctypes import c_longlong
from ctypes import c_float
from ctypes import Structure
from ctypes import POINTER
from ctypes import CFUNCTYPE

DRMAA2_CHAR_BUFFER_SIZE = 128

# Basic types.
drmaa2_time = c_longlong
drmaa2_enum = c_int
drmaa2_bool = drmaa2_enum
drmaa2_capability = drmaa2_enum
drmaa2_cpu = drmaa2_enum
drmaa2_error = drmaa2_enum
drmaa2_event = drmaa2_enum
drmaa2_listtype = drmaa2_enum
drmaa2_os = drmaa2_enum
drmaa2_jstate = drmaa2_enum


# drmaa2_string must be a subclass of c_char_p to allow us
# to free DRMAA2 strings.
class drmaa2_string(c_char_p):
    python_version = platform.python_version_tuple()[0]

    #    def __init__(self, **kwargs):
    #        """
    #        Ctypes.Structure with integrated default values.
    #
    #        :param kwargs: values different to defaults
    #        :type kwargs: dict
    #        """
    #        values = type(self)._defaults_.copy()
    #        for (key, val) in kwargs.items():
    #            values[key] = val
    #        super().__init__(**values)

    def __eq__(self, other):
        if isinstance(other, str):
            if self.python_version == '2':
                return self.value == other
            else:
                return self.value == other.encode()
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def encode(self):
        return self.value

    def decode(self):
        return self.value


# List types
drmaa2_list = c_void_p
drmaa2_string_list = drmaa2_list
drmaa2_j_list = drmaa2_list
drmaa2_queueinfo_list = drmaa2_list
drmaa2_machineinfo_list = drmaa2_list
drmaa2_slotinfo_list = drmaa2_list
drmaa2_r_list = drmaa2_list
drmaa2_list_entryfree = CFUNCTYPE(None, POINTER(c_void_p))

# Dict type
drmaa2_dict = c_void_p
drmaa2_dict_entryfree = CFUNCTYPE(None, POINTER(c_char_p), POINTER(c_char_p))


# DRMAA2 structs.
class drmaa2_struct(Structure):
    def __eq__(self, other):
        result = True
        for (attr_name, _) in self._fields_:
            a, b = getattr(self, attr_name), getattr(other, attr_name)
            if isinstance(a, ctypes.Array):
                if a[:] != b[:]:
                    result = False
                    break
            elif a != b:
                result = False
                break
        return result

    def __ne__(self, other):
        return not self.__eq__(other)


class drmaa2_sudo(drmaa2_struct):
    _fields_ = [("username", c_char * DRMAA2_CHAR_BUFFER_SIZE),
                ("groupname", c_char * DRMAA2_CHAR_BUFFER_SIZE),
                ("uid", c_long),
                ("gid", c_long)]


class drmaa2_jinfo(drmaa2_struct):
    _fields_ = [("jobId", drmaa2_string),
                ("jobName", drmaa2_string),
                ("exitStatus", c_int),
                ("terminatingSignal", drmaa2_string),
                ("annotation", drmaa2_string),
                ("jobState", drmaa2_jstate),
                ("jobSubState", drmaa2_string),
                ("allocatedMachines", drmaa2_slotinfo_list),
                ("submissionMachine", drmaa2_string),
                ("jobOwner", drmaa2_string),
                ("slots", c_longlong),
                ("queueName", drmaa2_string),
                ("wallclockTime", drmaa2_time),
                ("cpuTime", c_longlong),
                ("submissionTime", drmaa2_time),
                ("dispatchTime", drmaa2_time),
                ("finishTime", drmaa2_time),
                ("implementationSpecific", c_void_p)]


class drmaa2_slotinfo(drmaa2_struct):
    _fields_ = [("machineName", drmaa2_string),
                ("slots", c_longlong),
                ("implementationSpecific", c_void_p)]


class drmaa2_rinfo(drmaa2_struct):
    _fields_ = [("reservationId", drmaa2_string),
                ("reservationName", drmaa2_string),
                ("reservedStartTime", drmaa2_time),
                ("reservedEndTime", drmaa2_time),
                ("usersACL", drmaa2_string_list),
                ("reservedSlots", c_longlong),
                ("reservedMachines", drmaa2_slotinfo_list),
                ("implementationSpecific", c_void_p)]


class drmaa2_jtemplate(drmaa2_struct):
    _fields_ = [("remoteCommand", drmaa2_string),
                ("args", drmaa2_string_list),
                ("submitAsHold", drmaa2_bool),
                ("rerunnable", drmaa2_bool),
                ("jobEnvironment", drmaa2_dict),
                ("workingDirectory", drmaa2_string),
                ("jobCategory", drmaa2_string),
                ("email", drmaa2_string_list),
                ("emailOnStarted", drmaa2_bool),
                ("emailOnTerminated", drmaa2_bool),
                ("jobName", drmaa2_string),
                ("inputPath", drmaa2_string),
                ("outputPath", drmaa2_string),
                ("errorPath", drmaa2_string),
                ("joinFiles", drmaa2_bool),
                ("reservationId", drmaa2_string),
                ("queueName", drmaa2_string),
                ("minSlots", c_longlong),
                ("maxSlots", c_longlong),
                ("priority", c_longlong),
                ("candidateMachines", drmaa2_string_list),
                ("minPhysMemory", c_longlong),
                ("machineOS", drmaa2_os),
                ("machineArch", drmaa2_cpu),
                ("startTime", drmaa2_time),
                ("deadlineTime", drmaa2_time),
                ("stageInFiles", drmaa2_dict),
                ("stageOutFiles", drmaa2_dict),
                ("resourceLimits", drmaa2_dict),
                ("accountingId", drmaa2_string),
                ("implementationSpecific", c_void_p)]


class drmaa2_rtemplate(drmaa2_struct):
    _fields_ = [("reservationName", drmaa2_string),
                ("startTime", drmaa2_time),
                ("endTime", drmaa2_time),
                ("duration", drmaa2_time),
                ("minSlots", c_longlong),
                ("maxSlots", c_longlong),
                ("jobCategory", drmaa2_string),
                ("usersACL", drmaa2_string_list),
                ("candidateMachines", drmaa2_string_list),
                ("minPhysMemory", c_longlong),
                ("machineOS", drmaa2_os),
                ("machineArch", drmaa2_cpu),
                ("implementationSpecific", c_void_p)]


class drmaa2_notification(drmaa2_struct):
    _fields_ = [("event", drmaa2_event),
                ("jobId", drmaa2_string),
                ("sessionName", drmaa2_string),
                ("jobState", drmaa2_jstate),
                ("implementationSpecific", c_void_p)]


class drmaa2_queueinfo(drmaa2_struct):
    _fields_ = [("name", drmaa2_string),
                ("implementationSpecific", c_void_p)]


class drmaa2_version(drmaa2_struct):
    _fields_ = [("major", drmaa2_string),
                ("minor", drmaa2_string),
                ("implementationSpecific", c_void_p)]


class drmaa2_machineinfo(drmaa2_struct):
    _fields_ = [("name", drmaa2_string),
                ("available", drmaa2_bool),
                ("sockets", c_longlong),
                ("coresPerSocket", c_longlong),
                ("threadsPerCore", c_longlong),
                ("load", c_float),
                ("physMemory", c_longlong),
                ("virtMemory", c_longlong),
                ("machineArch", drmaa2_cpu),
                ("machineOSVersion", POINTER(drmaa2_version)),
                ("machineOS", drmaa2_os),
                ("implementationSpecific", c_void_p)]


# Callback function
drmaa2_callback = CFUNCTYPE(None, POINTER(drmaa2_notification))


# UGE-specific structs
class drmaa2_j(drmaa2_struct):
    _fields_ = [("id", drmaa2_string),
                ("session_name", drmaa2_string),
                ("job_name", drmaa2_string)]


class drmaa2_jarray(drmaa2_struct):
    _fields_ = [("id", drmaa2_string),
                ("job_list", drmaa2_j_list),
                ("session_name", drmaa2_string)]


class drmaa2_jsession(drmaa2_struct):
    _fields_ = [("contact", drmaa2_string),
                ("name", drmaa2_string)]


class drmaa2_msession(drmaa2_struct):
    _fields_ = [("name", drmaa2_string)]


class drmaa2_r(drmaa2_struct):
    _fields_ = [("id", drmaa2_string),
                ("session_name", drmaa2_string)]


class drmaa2_rsession(drmaa2_struct):
    _fields_ = [("contact", drmaa2_string),
                ("name", drmaa2_string)]


#######################################################################
# Test.
if __name__ == '__main__':
    pass
