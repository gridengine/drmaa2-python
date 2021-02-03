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

"""
Definitions for DRMAA2 exception classes.
"""

from .drmaa2_constants import StatusCode


class Drmaa2Exception(Exception):
    """ 
    Base class for all DRMAA2 exceptions. 

    Usage examples:
    
    >>> raise Drmaa2Exception(error_message, error_code)
    """

    def __init__(self, error='', error_code=StatusCode.UNSET_ERROR):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str

        :param error_code: Error code.
        :type error_code: int
        """
        Exception.__init__(self, error)
        self.error_code = error_code


class DeniedByDrms(Drmaa2Exception):
    """ DRM denied the operation. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.DENIED_BY_DRMS)


class DrmCommunicationError(Drmaa2Exception):
    """ DRM could not be contacted. The problem may or may not be transient. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.DRM_COMMUNICATION)


class TryLaterError(Drmaa2Exception):
    """ An error due to a transient problem that can be retried. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.TRY_LATER)


class SessionManagementError(Drmaa2Exception):
    """ Session management error. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.SESSION_MANAGEMENT)


class TimeoutError(Drmaa2Exception):
    """ Operation timed out. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.TIMEOUT)


class InternalError(Drmaa2Exception):
    """ DRMAA2 Internal error. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.INTERNAL)


class InvalidArgument(Drmaa2Exception):
    """ Invalid argument error. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.INVALID_ARGUMENT)


class InvalidSession(Drmaa2Exception):
    """ Invalid (e.g., previously closed) session used for the operation. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.INVALID_SESSION)


class InvalidState(Drmaa2Exception):
    """ Operation is not allowed given the current state of the job. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.INVALID_STATE)


class ResourceNotAvailable(Drmaa2Exception):
    """ Requested resource is not available. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.OUT_OF_RESOURCE)


class UnsupportedAttribute(Drmaa2Exception):
    """ The given attribute is not supported by the DRMAA2 implementation. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.UNSUPPORTED_ATTRIBUTE)


class UnsupportedOperation(Drmaa2Exception):
    """ The given operation is not supported by the DRMAA2 implementation. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.UNSUPPORTED_OPERATION)


class ImplementationSpecificError(Drmaa2Exception):
    """ Implementation-specific error condition. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.IMPLEMENTATION_SPECIFIC)


class AuthorizationError(Drmaa2Exception):
    """ Authorization error. """

    def __init__(self, error=''):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str
        """
        Drmaa2Exception.__init__(self, error=error, error_code=StatusCode.AUTHORIZATION)
