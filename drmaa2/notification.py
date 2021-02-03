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

import atexit
from ctypes import POINTER

from .drmaa2_ctypes import drmaa2_callback
from .byte_string import ByteString
from .drmaa2_constants import Event
from .drmaa2_constants import JobState
from .drmaa2_object import Drmaa2Object
from .drmaa2_exceptions import InvalidArgument

from .log_manager import LogManager
from .exception_mapper import ExceptionMapper


class Notification(Drmaa2Object):
    """ High-level DRMAA2 notification class. """

    event = Drmaa2Object.EnumDescriptor('event', Event)
    """ Event number (Event). """
    session_name = Drmaa2Object.StringDescriptor('sessionName')
    """ Session name (str). """
    job_id = Drmaa2Object.StringDescriptor('jobId')
    """ Job id (str). """
    job_state = Drmaa2Object.EnumDescriptor('jobState', JobState)
    """ Job state (JobState). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    logger = LogManager.get_instance().get_logger('Notification')

    def __init__(self, notification):
        """ 
        Constructor. 
        """
        Drmaa2Object.__init__(self)
        if isinstance(notification, POINTER(drmaa2_notification)):
            self._struct = POINTER(drmaa2_notification)()
            self._struct.contents = drmaa2_notification()
            self.event = getattr(notification.contents, 'event')
            self.job_id = ByteString(getattr(notification.contents, 'jobId').value).decode()
            self.session_name = ByteString(getattr(notification.contents, 'sessionName').value).decode()
            self.job_state = getattr(notification.contents, 'jobState')
            self.implementation_specific = getattr(notification.contents, 'implementationSpecific')
        else:
            raise InvalidArgument('Invalid argument: %s' % str(notification))
        self._read_only = True

    def __del__(self):
        pass

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.

        >>> print(Notification.get_implementation_specific_keys())
        []
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(
                cls.get_drmaa2_library().drmaa2_notification_impl_spec())
        return cls.implementation_specific_keys

    @classmethod
    def event_callback(cls, callback):
        """ Wrap actual python callback. """

        def wrapper(notification_ptr):
            notification = Notification(notification_ptr.contents)
            callback(notification)
            cls.get_drmaa2_library().drmaa2_notification_free(notification_ptr)

        return wrapper

    @classmethod
    def register_event_notification(cls, callback):
        """
        Register callback for event notifications.

        :param callback: Callback function.
        :type callback: Function pointer.

        >>> def event_callback(notification):         
        ...     print('Event %s for job %s' % (notification.event, notification.job_id)) 
        >>> Notification.register_event_notification(event_callback)
        """
        callback_p = drmaa2_callback(cls.event_callback(callback))
        cls.logger.debug("Registering notification callback {}".format(callback_p))
        ExceptionMapper.check_status_code(cls.get_drmaa2_library().drmaa2_register_event_notification(callback_p))
        atexit.register(unregister_event_notification)

    @classmethod
    def unregister_event_notification(cls):
        """
        Unregister callback for event notifications.

        >>> Notification.unregister_event_notification()
        """
        callback_p = drmaa2_callback()
        cls.logger.debug("Unregistering notification callback {}".format(callback_p))
        ExceptionMapper.check_status_code(cls.get_drmaa2_library().drmaa2_register_event_notification(callback_p))
