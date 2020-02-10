#___INFO__MARK_BEGIN__
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
#___INFO__MARK_END__
from .drmaa2_constants import (Bool, Capability, Cpu, Event, JobState, 
    ListType, Os, ResourceLimit, StatusCode, Time)
from .drmaa2_exceptions import (Drmaa2Exception, DeniedByDrms,
    DrmCommunicationError, TryLaterError, SessionManagementError, 
    TimeoutError, InternalError, InvalidArgument, 
    InvalidSession, InvalidState, ResourceNotAvailable, 
    UnsupportedAttribute, UnsupportedOperation,
    ImplementationSpecificError, AuthorizationError)
from .library_manager import LibraryManager
from .log_manager import LogManager
from .job_session import JobSession
from .job_info import JobInfo
from .job_array import JobArray
from .job_template import JobTemplate
from .job import Job
from .reservation_session import ReservationSession
from .reservation_template import ReservationTemplate
from .reservation_info import ReservationInfo
from .reservation import Reservation
from .sudo import Sudo
from .version import Version
from .monitoring_session import MonitoringSession
from .machine_info import MachineInfo
from .queue_info import QueueInfo
from .notification import Notification

get_drms_name = LibraryManager.get_drms_name
get_drmaa_name = LibraryManager.get_drmaa_name
drmaa_supports = LibraryManager.drmaa_supports 
get_drms_version = Version.get_drms_version
get_drmaa_version = Version.get_drmaa_version
get_job_session_names = JobSession.list_session_names 
get_reservation_session_names = ReservationSession.list_session_names 
 
__version__ = '8.6.10'
