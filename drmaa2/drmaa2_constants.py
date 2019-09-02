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
Definitions for various DRMAA2 constants, including enums.
"""

from datetime import datetime
from enum import Enum
from enum import IntEnum

UNSET_BOOL = 0
UNSET_ENUM = -1
UNSET_NUM = -1
UNSET_PRIORITY = -99999
UNSET_TIME = -3

POSIX_EPOCH = datetime.utcfromtimestamp(0)
PY_DICT_TYPE = type(dict())
PY_STRING_TYPE = type('string')
PY_BYTES_TYPE = type(b'string')


class Bool(IntEnum):
    """ DRMAA2 Bool enum. """
    FALSE = 0
    TRUE = 1


class Time(IntEnum):
    """ DRMAA2 Time enum. """
    ZERO_TIME = 0
    INFINITE_TIME = -1
    NOW = -2
    UNSET_TIME = -3


class Capability(IntEnum):
    """ DRMAA2 Capabilities enum. """
    UNSET_CAPABILITY = -1
    ADVANCE_RESERVATION = 0
    RESERVE_SLOTS = 1
    CALLBACK = 2
    BULK_JOBS_MAXPARALLEL = 3
    JT_EMAIL = 4
    JT_STAGING = 5
    JT_DEADLINE = 6
    JT_MAXSLOTS = 7
    JT_ACCOUNTINGID = 8
    RT_STARTNOW = 9
    RT_DURATION = 10
    RT_MACHINEOS = 11
    RT_MACHINEARCH = 12


class Cpu(IntEnum):
    """ DRMAA2 CPU enum. """
    UNSET_CPU = -1
    OTHER_CPU = 0
    ALPHA = 1
    ARM = 2
    ARM64 = 3
    CELL = 4
    PARISC = 5
    PARISC64 = 6
    X86 = 7
    X64 = 8
    IA64 = 9
    MIPS = 10
    MIPS64 = 11
    PPC = 12
    PPC64 = 13
    SPARC = 14
    SPARC64 = 15
    PPC64LE = 16


class Event(IntEnum):
    """ DRMAA2 event enum. """
    UNSET_EVENT = -1
    NEW_STATE = 0
    MIGRATED = 1
    ATTRIBUTE_CHANGE = 2


class JobState(IntEnum):
    """ DRMAA2 job state enum. """
    UNSET_JSTATE = -1
    UNDETERMINED = 0
    QUEUED = 1
    QUEUED_HELD = 2
    RUNNING = 3
    SUSPENDED = 4
    REQUEUED = 5
    REQUEUED_HELD = 6
    DONE = 7
    FAILED = 8
    RUNNING_HELD = 9


class Os(IntEnum):
    """ DRMAA2 OS enum. """
    UNSET_OS = -1
    OTHER_OS = 0
    AIX = 1
    BSD = 2
    LINUX = 3
    HPUX = 4
    IRIX = 5
    MACOS = 6
    SUNOS = 7
    TRU64 = 8
    UNIXWARE = 9
    WIN = 10
    WINNT = 11


class ResourceLimit(Enum):
    """ DRMAA2 resource limits enum. """
    CORE_FILE_SIZE = "CORE_FILE_SIZE"
    CPU_TIME = "CPU_TIME"
    DATA_SIZE = "DATA_SIZE"
    FILE_SIZE = "FILE_SIZE"
    OPEN_FILES = "OPEN_FILES"
    STACK_SIZE = "STACK_SIZE"
    VIRTUAL_MEMORY = "VIRTUAL_MEMORY"
    WALLCLOCK_TIME = "WALLCLOCK_TIME"


class ListType(IntEnum):
    """ DRMAA2 list type enum. """
    UNSET_LISTTYPE = -1
    STRINGLIST = 0
    JOBLIST = 1
    QUEUEINFOLIST = 2
    MACHINEINFOLIST = 3
    SLOTINFOLIST = 4
    RESERVATIONLIST = 5


class StatusCode(IntEnum):
    """ DRMAA2 status code enum. """
    UNSET_ERROR = -1
    SUCCESS = 0
    DENIED_BY_DRMS = 1
    DRM_COMMUNICATION = 2
    TRY_LATER = 3
    SESSION_MANAGEMENT = 4
    TIMEOUT = 5
    INTERNAL = 6
    INVALID_ARGUMENT = 7
    INVALID_SESSION = 8
    INVALID_STATE = 9
    OUT_OF_RESOURCE = 10
    UNSUPPORTED_ATTRIBUTE = 11
    UNSUPPORTED_OPERATION = 12
    IMPLEMENTATION_SPECIFIC = 13
    AUTHORIZATION = 14
    LASTERROR = 15
