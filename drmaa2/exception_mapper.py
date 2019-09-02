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
Exception mapper class.
"""

from .byte_string import ByteString
from .drmaa2_constants import StatusCode
from .drmaa2_exceptions import Drmaa2Exception
from .drmaa2_exceptions import DeniedByDrms
from .drmaa2_exceptions import DrmCommunicationError
from .drmaa2_exceptions import TryLaterError
from .drmaa2_exceptions import SessionManagementError
from .drmaa2_exceptions import TimeoutError
from .drmaa2_exceptions import InternalError
from .drmaa2_exceptions import InvalidArgument
from .drmaa2_exceptions import InvalidSession
from .drmaa2_exceptions import InvalidState
from .drmaa2_exceptions import ResourceNotAvailable
from .drmaa2_exceptions import UnsupportedAttribute
from .drmaa2_exceptions import UnsupportedOperation
from .drmaa2_exceptions import ImplementationSpecificError
from .drmaa2_exceptions import AuthorizationError
from .library_manager import LibraryManager


class ExceptionMapper(object):
    EXCEPTION_MAP = {
        StatusCode.UNSET_ERROR: Drmaa2Exception,
        StatusCode.SUCCESS: None,
        StatusCode.DENIED_BY_DRMS: DeniedByDrms,
        StatusCode.DRM_COMMUNICATION: DrmCommunicationError,
        StatusCode.TRY_LATER: TryLaterError,
        StatusCode.SESSION_MANAGEMENT: SessionManagementError,
        StatusCode.TIMEOUT: TimeoutError,
        StatusCode.INTERNAL: InternalError,
        StatusCode.INVALID_ARGUMENT: InvalidArgument,
        StatusCode.INVALID_SESSION: InvalidSession,
        StatusCode.INVALID_STATE: InvalidState,
        StatusCode.OUT_OF_RESOURCE: ResourceNotAvailable,
        StatusCode.UNSUPPORTED_ATTRIBUTE: UnsupportedAttribute,
        StatusCode.UNSUPPORTED_OPERATION: UnsupportedOperation,
        StatusCode.IMPLEMENTATION_SPECIFIC: ImplementationSpecificError,
        StatusCode.AUTHORIZATION: AuthorizationError,
    }

    @classmethod
    def get_last_error_message(cls):
        """ 
        Retrieve the last error from the DRMAA2 library.

        :return str: Last error message
        """
        drmaa2_lib = LibraryManager.get_instance().get_drmaa2_library()
        string_ptr = drmaa2_lib.drmaa2_lasterror_text()
        message = ''
        if string_ptr:
            message = ByteString(string_ptr.value).decode()
            drmaa2_lib.drmaa2_string_free(string_ptr)
        return message

    @classmethod
    def last_error_code(cls):
        """ 
        Retrieve the last error code from the DRMAA2 library.

        :return int: Last error number
        """
        drmaa2_lib = LibraryManager.get_instance().get_drmaa2_library()
        return drmaa2_lib.drmaa2_lasterror()

    @classmethod
    def check_last_error_code(cls):
        """ 
        Check the last error code from the DRMAA2 library.

        :raises Drmaa2Exception: in case of a non-zero code
        """
        code = cls.last_error_code()
        cls.check_status_code(code)

    @classmethod
    def check_status_code(cls, code):
        """ 
        Check the last error code from the DRMAA2 library.

        :raises Drmaa2Exception: in case of a non-zero code
        """
        status_code = StatusCode(code)
        if status_code != StatusCode.SUCCESS:
            error_class = cls.EXCEPTION_MAP.get(status_code, Drmaa2Exception)
            error = error_class(error=cls.get_last_error_message())
            raise error


#######################################################################
# Test.
if __name__ == '__main__':
    ExceptionMapper.check_last_error_code()
    ExceptionMapper.check_status_code(5)
