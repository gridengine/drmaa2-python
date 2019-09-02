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

import os
import glob
import platform
import ctypes
import ctypes.util
from ctypes import c_char_p
from ctypes import c_void_p
from ctypes import c_long
from ctypes import c_longlong
from ctypes import POINTER
from ctypes import pointer

from .drmaa2_ctypes import drmaa2_error
from .drmaa2_ctypes import drmaa2_bool
from .drmaa2_ctypes import drmaa2_capability

from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_string_list
from .drmaa2_ctypes import drmaa2_list
from .drmaa2_ctypes import drmaa2_listtype
from .drmaa2_ctypes import drmaa2_list_entryfree
from .drmaa2_ctypes import drmaa2_dict
from .drmaa2_ctypes import drmaa2_dict_entryfree

from .drmaa2_ctypes import drmaa2_j
from .drmaa2_ctypes import drmaa2_j_list
from .drmaa2_ctypes import drmaa2_jarray
from .drmaa2_ctypes import drmaa2_jinfo
from .drmaa2_ctypes import drmaa2_jtemplate
from .drmaa2_ctypes import drmaa2_jstate

from .drmaa2_ctypes import drmaa2_r
from .drmaa2_ctypes import drmaa2_r_list
from .drmaa2_ctypes import drmaa2_rinfo
from .drmaa2_ctypes import drmaa2_rtemplate

from .drmaa2_ctypes import drmaa2_slotinfo
from .drmaa2_ctypes import drmaa2_queueinfo
from .drmaa2_ctypes import drmaa2_queueinfo_list

from .drmaa2_ctypes import drmaa2_machineinfo
from .drmaa2_ctypes import drmaa2_machineinfo_list

from .drmaa2_ctypes import drmaa2_jsession
from .drmaa2_ctypes import drmaa2_rsession
from .drmaa2_ctypes import drmaa2_msession

from .drmaa2_ctypes import drmaa2_sudo
from .drmaa2_ctypes import drmaa2_notification
from .drmaa2_ctypes import drmaa2_version
from .drmaa2_ctypes import drmaa2_time
from .drmaa2_ctypes import drmaa2_callback

from .byte_string import ByteString
from .log_manager import LogManager
from .singleton import Singleton
from .drmaa2_exceptions import Drmaa2Exception


class LibraryManager(Singleton):
    """ 
    Singleton class for loading and keeping reference to the
    underlying C library.
    """

    logger = LogManager.get_instance().get_logger('LibraryManager')

    __instance = None

    def __init__(self):
        """
        Constructor. 

        >>> lm = LibraryManager()
        """
        if LibraryManager.__instance:
            return
        LibraryManager.__instance = self
        self.drmaa2_library = self.__load_drmaa2_library()

    def get_drmaa2_library(self):
        """
        Get reference to the DRMAA2 C library.

        >>> drmaa2_lib = LibraryManager.get_instance().get_drmaa2_library()
        """
        return self.drmaa2_library

    def to_py_string(self, ctypes_string):
        py_string = ByteString(ctypes_string.value).decode()
        self.drmaa2_library.drmaa2_string_free(pointer(ctypes_string))
        return py_string

    @classmethod
    def get_drms_name(cls):
        """
        Retrieve DRMS name.

        :returns: DRMS name

        >>> print(LibraryManager.get_drms_name())
        Univa Grid Engine
        """
        lm = LibraryManager.get_instance()
        ctypes_string = lm.get_drmaa2_library().drmaa2_get_drms_name();
        return lm.to_py_string(ctypes_string)

    @classmethod
    def get_drmaa_name(cls):
        """
        Retrieve DRMAA name.

        :returns: DRMAA name

        >>> print(LibraryManager.get_drmaa_name())
        Univa Grid Engine Drmaa V2
        """
        lm = LibraryManager.get_instance()
        ctypes_string = lm.get_drmaa2_library().drmaa2_get_drmaa_name();
        return lm.to_py_string(ctypes_string)

    @classmethod
    def drmaa_supports(cls, capability):
        """
        Check whether the library supports given capability/

        :returns: True if capability is supported, false otherwise.

        >>> print(LibraryManager.drmaa_supports(Capability.JT_EMAIL))
        True
        """
        lm = LibraryManager.get_instance()
        c = capability
        return lm.get_drmaa2_library().drmaa2_supports(int(c)) > 0;

    @classmethod
    def __load_drmaa2_library(cls):
        cls.logger.debug('Loading DRMAA2 library')
        libc_name = ctypes.util.find_library('c')
        libc = ctypes.CDLL(libc_name)
        libc.memcmp.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
        lib_path = 'libdrmaa2.so'
        drmaa2_lib = None
        try:
            SGE_ROOT = os.environ['SGE_ROOT']
            SGE_ARCH = os.popen(SGE_ROOT + '/util/arch').read().rstrip()
            lib_dir = SGE_ROOT + '/lib/' + SGE_ARCH
            cls.logger.debug('Looking for DRMAA2 library under %s' % lib_dir)
            lib_paths = glob.glob(lib_dir + '/libdrmaa2.so')
            if not lib_paths:
                lib_paths = glob.glob(lib_dir + '/libdrmaa2.dylib')
            if len(lib_paths):
                lib_path = lib_paths[0]
            else:
                cls.logger.warn('Could not find DRMAA2 library under %s' % lib_dir)
        except KeyError:
            cls.logger.debug('SGE_ROOT is not defined')
        cls.logger.debug('Library path: %s' % lib_path)

        try:
            drmaa2_lib = ctypes.cdll.LoadLibrary(str(lib_path))
        except OSError:
            raise Drmaa2Exception('Could not load DRMAA2 library.')

        cls.logger.debug("Initializing DRMAA2 library")

        drmaa2_lib.drmaa2_string_free.restype = None
        drmaa2_lib.drmaa2_string_free.argtypes = [POINTER(drmaa2_string)]

        drmaa2_lib.drmaa2_list_create.restype = drmaa2_list
        drmaa2_lib.drmaa2_list_create.argtypes = [drmaa2_listtype, drmaa2_list_entryfree]
        drmaa2_lib.drmaa2_list_free.restype = None
        drmaa2_lib.drmaa2_list_free.argtypes = [POINTER(drmaa2_list)]
        drmaa2_lib.drmaa2_list_get.restype = c_void_p
        drmaa2_lib.drmaa2_list_get.argtypes = [drmaa2_list, c_long]
        drmaa2_lib.drmaa2_list_add.restype = drmaa2_error
        drmaa2_lib.drmaa2_list_add.argtypes = [drmaa2_list, c_void_p]
        drmaa2_lib.drmaa2_list_del.restype = drmaa2_error
        drmaa2_lib.drmaa2_list_del.argtypes = [drmaa2_list, c_long]
        drmaa2_lib.drmaa2_list_size.restype = c_long
        drmaa2_lib.drmaa2_list_size.argtypes = [drmaa2_list]

        drmaa2_lib.drmaa2_lasterror.restype = drmaa2_error
        drmaa2_lib.drmaa2_lasterror.argtypes = []
        drmaa2_lib.drmaa2_lasterror_text.restype = drmaa2_string
        drmaa2_lib.drmaa2_lasterror_text.argtypes = []

        # UGE-specific
        drmaa2_lib.uge_drmaa2_list_free_root.restype = None
        drmaa2_lib.uge_drmaa2_list_free_root.argtypes = [POINTER(drmaa2_list)]
        drmaa2_lib.uge_drmaa2_list_set.restype = drmaa2_error
        drmaa2_lib.uge_drmaa2_list_set.argtypes = [drmaa2_list, c_long, c_void_p]

        drmaa2_lib.uge_vi_impl_spec_get.restype = drmaa2_dict
        drmaa2_lib.uge_vi_impl_spec_get.argtypes = [POINTER(drmaa2_version)]

        drmaa2_lib.drmaa2_dict_create.restype = drmaa2_dict
        drmaa2_lib.drmaa2_dict_create.argtypes = [drmaa2_dict_entryfree]
        drmaa2_lib.drmaa2_dict_free.restype = None
        drmaa2_lib.drmaa2_dict_free.argtypes = [POINTER(drmaa2_dict)]
        drmaa2_lib.drmaa2_dict_list.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_dict_list.argtypes = [drmaa2_dict]
        drmaa2_lib.drmaa2_dict_has.restype = drmaa2_bool
        drmaa2_lib.drmaa2_dict_has.argtypes = [drmaa2_dict, c_char_p]
        drmaa2_lib.drmaa2_dict_get.restype = c_char_p
        drmaa2_lib.drmaa2_dict_get.argtypes = [drmaa2_dict, c_char_p]
        drmaa2_lib.drmaa2_dict_del.restype = drmaa2_error
        drmaa2_lib.drmaa2_dict_del.argtypes = [drmaa2_dict, c_char_p]
        drmaa2_lib.drmaa2_dict_set.restype = drmaa2_error
        drmaa2_lib.drmaa2_dict_set.argtypes = [drmaa2_dict, c_char_p]

        drmaa2_lib.drmaa2_jinfo_create.restype = POINTER(drmaa2_jinfo)
        drmaa2_lib.drmaa2_jinfo_create.argtypes = []
        drmaa2_lib.drmaa2_jinfo_free.restype = None
        drmaa2_lib.drmaa2_jinfo_free.argtypes = [POINTER(POINTER(drmaa2_jinfo))]

        drmaa2_lib.drmaa2_slotinfo_free.restype = None
        drmaa2_lib.drmaa2_slotinfo_free.argtypes = [POINTER(POINTER(drmaa2_slotinfo))]

        drmaa2_lib.drmaa2_rinfo_create.restype = POINTER(drmaa2_rinfo)
        drmaa2_lib.drmaa2_rinfo_create.argtypes = []
        drmaa2_lib.drmaa2_rinfo_free.restype = None
        drmaa2_lib.drmaa2_rinfo_free.argtypes = [POINTER(POINTER(drmaa2_rinfo))]

        drmaa2_lib.drmaa2_jtemplate_create.restype = POINTER(drmaa2_jtemplate)
        drmaa2_lib.drmaa2_jtemplate_create.argtypes = []
        drmaa2_lib.drmaa2_jtemplate_free.restype = None
        drmaa2_lib.drmaa2_jtemplate_free.argtypes = [POINTER(POINTER(drmaa2_jtemplate))]

        drmaa2_lib.drmaa2_rtemplate_create.restype = POINTER(drmaa2_rtemplate)
        drmaa2_lib.drmaa2_rtemplate_create.argtypes = []
        drmaa2_lib.drmaa2_rtemplate_free.restype = None
        drmaa2_lib.drmaa2_rtemplate_free.argtypes = [POINTER(POINTER(drmaa2_rtemplate))]

        drmaa2_lib.drmaa2_queueinfo_free.restype = None
        drmaa2_lib.drmaa2_queueinfo_free.argtypes = [POINTER(POINTER(drmaa2_queueinfo))]

        drmaa2_lib.drmaa2_machineinfo_free.restype = None
        drmaa2_lib.drmaa2_machineinfo_free.argtypes = [POINTER(POINTER(drmaa2_machineinfo))]

        drmaa2_lib.drmaa2_notification_free.restype = None
        drmaa2_lib.drmaa2_notification_free.argtypes = [POINTER(POINTER(drmaa2_notification))]

        drmaa2_lib.drmaa2_version_free.restype = None
        drmaa2_lib.drmaa2_version_free.argtypes = [POINTER(POINTER(drmaa2_version))]

        drmaa2_lib.drmaa2_jtemplate_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_jtemplate_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_jinfo_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_jinfo_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_rtemplate_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_rtemplate_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_rinfo_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_rinfo_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_queueinfo_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_queueinfo_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_machineinfo_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_machineinfo_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_notification_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_notification_impl_spec.argtypes = []
        drmaa2_lib.drmaa2_version_impl_spec.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_version_impl_spec.argtypes = []

        drmaa2_lib.drmaa2_get_instance_value.restype = drmaa2_string
        drmaa2_lib.drmaa2_get_instance_value.argtypes = [c_void_p, c_char_p]
        drmaa2_lib.drmaa2_describe_attribute.restype = drmaa2_string
        drmaa2_lib.drmaa2_describe_attribute.argtypes = [c_void_p, c_char_p]
        drmaa2_lib.drmaa2_set_instance_value.restype = drmaa2_error
        drmaa2_lib.drmaa2_set_instance_value.argtypes = [c_void_p, c_char_p, c_char_p]

        drmaa2_lib.drmaa2_jsession_free.restype = None
        drmaa2_lib.drmaa2_jsession_free.argtypes = [POINTER(POINTER(drmaa2_jsession))]
        drmaa2_lib.drmaa2_rsession_free.restype = None
        drmaa2_lib.drmaa2_rsession_free.argtypes = [POINTER(POINTER(drmaa2_rsession))]
        drmaa2_lib.drmaa2_msession_free.restype = None
        drmaa2_lib.drmaa2_msession_free.argtypes = [POINTER(POINTER(drmaa2_msession))]

        drmaa2_lib.drmaa2_j_free.restype = None
        drmaa2_lib.drmaa2_j_free.argtypes = [POINTER(POINTER(drmaa2_j))]
        drmaa2_lib.drmaa2_jarray_free.restype = None
        drmaa2_lib.drmaa2_jarray_free.argtypes = [POINTER(POINTER(drmaa2_jarray))]
        drmaa2_lib.drmaa2_r_free.restype = None
        drmaa2_lib.drmaa2_r_free.argtypes = [POINTER(POINTER(drmaa2_r))]

        drmaa2_lib.drmaa2_rsession_get_contact.restype = drmaa2_string
        drmaa2_lib.drmaa2_rsession_get_contact.argtypes = [drmaa2_rsession]
        drmaa2_lib.drmaa2_rsession_get_session_name.restype = drmaa2_string
        drmaa2_lib.drmaa2_rsession_get_session_name.argtypes = [drmaa2_rsession]
        drmaa2_lib.drmaa2_rsession_get_reservation.restype = POINTER(drmaa2_r)
        drmaa2_lib.drmaa2_rsession_get_reservation.argtypes = [POINTER(drmaa2_rsession), drmaa2_string]
        drmaa2_lib.drmaa2_rsession_request_reservation.restype = POINTER(drmaa2_r)
        drmaa2_lib.drmaa2_rsession_request_reservation.argtypes = [POINTER(drmaa2_rsession), POINTER(drmaa2_rtemplate)]
        drmaa2_lib.drmaa2_rsession_request_reservation_as.restype = POINTER(drmaa2_r)
        drmaa2_lib.drmaa2_rsession_request_reservation_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_rsession),
                                                                      POINTER(drmaa2_rtemplate)]

        drmaa2_lib.drmaa2_rsession_get_reservations.restype = drmaa2_r_list
        drmaa2_lib.drmaa2_rsession_get_reservations.argtypes = [POINTER(drmaa2_rsession)]

        drmaa2_lib.drmaa2_r_get_id.restype = drmaa2_string
        drmaa2_lib.drmaa2_r_get_id.argtypes = [drmaa2_r]
        drmaa2_lib.drmaa2_r_get_session_name.restype = drmaa2_string
        drmaa2_lib.drmaa2_r_get_session_name.argtypes = [drmaa2_r]
        # drmaa2_lib.drmaa2_r_get_reservation_template.restype = POINTER(drmaa2_rtemplate)
        # drmaa2_lib.drmaa2_r_get_reservation_template.argtypes = [POINTER(drmaa2_r)]
        drmaa2_lib.drmaa2_r_get_rtemplate.restype = POINTER(drmaa2_rtemplate)
        drmaa2_lib.drmaa2_r_get_rtemplate.argtypes = [POINTER(drmaa2_r)]
        drmaa2_lib.drmaa2_r_get_info.restype = POINTER(drmaa2_rinfo)
        drmaa2_lib.drmaa2_r_get_info.argtypes = [POINTER(drmaa2_r)]
        drmaa2_lib.drmaa2_r_terminate.restype = drmaa2_error
        drmaa2_lib.drmaa2_r_terminate.argtypes = [POINTER(drmaa2_r)]
        drmaa2_lib.drmaa2_r_terminate_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_r_terminate_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_r)]

        drmaa2_lib.drmaa2_jarray_get_id.restype = drmaa2_string
        drmaa2_lib.drmaa2_jarray_get_id.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_get_jobs.restype = drmaa2_j_list
        drmaa2_lib.drmaa2_jarray_get_jobs.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_get_session_name.restype = drmaa2_string
        drmaa2_lib.drmaa2_jarray_get_session_name.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_get_jtemplate.restype = POINTER(drmaa2_jtemplate)
        drmaa2_lib.drmaa2_jarray_get_jtemplate.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_suspend.restype = drmaa2_error
        drmaa2_lib.drmaa2_jarray_suspend.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_resume.restype = drmaa2_error
        drmaa2_lib.drmaa2_jarray_resume.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_hold.restype = drmaa2_error
        drmaa2_lib.drmaa2_jarray_hold.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_release.restype = drmaa2_error
        drmaa2_lib.drmaa2_jarray_release.argtypes = [POINTER(drmaa2_jarray)]
        drmaa2_lib.drmaa2_jarray_terminate.restype = drmaa2_error
        drmaa2_lib.drmaa2_jarray_terminate.argtypes = [POINTER(drmaa2_jarray)]

        drmaa2_lib.drmaa2_jsession_get_contact.restype = drmaa2_string
        drmaa2_lib.drmaa2_jsession_get_contact.argtypes = [POINTER(drmaa2_jsession)]
        drmaa2_lib.drmaa2_jsession_get_session_name.restype = drmaa2_string
        drmaa2_lib.drmaa2_jsession_get_session_name.argtypes = [POINTER(drmaa2_jsession)]
        drmaa2_lib.drmaa2_jsession_get_job_categories.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_jsession_get_job_categories.argtypes = [POINTER(drmaa2_jsession)]
        drmaa2_lib.drmaa2_jsession_get_jobs.restype = drmaa2_j_list
        drmaa2_lib.drmaa2_jsession_get_jobs.argtypes = [POINTER(drmaa2_jsession), POINTER(drmaa2_jinfo)]
        drmaa2_lib.drmaa2_jsession_get_job_array.restype = POINTER(drmaa2_jarray)
        drmaa2_lib.drmaa2_jsession_get_job_array.argtypes = [POINTER(drmaa2_jsession), drmaa2_string]
        drmaa2_lib.drmaa2_jsession_run_job.restype = POINTER(drmaa2_j)
        drmaa2_lib.drmaa2_jsession_run_job.argtypes = [POINTER(drmaa2_jsession), POINTER(drmaa2_jtemplate)]
        drmaa2_lib.drmaa2_jsession_run_job_as.restype = POINTER(drmaa2_j)
        drmaa2_lib.drmaa2_jsession_run_job_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_jsession),
                                                          POINTER(drmaa2_jtemplate)]
        drmaa2_lib.drmaa2_jsession_run_bulk_jobs.restype = POINTER(drmaa2_jarray)
        drmaa2_lib.drmaa2_jsession_run_bulk_jobs.argtypes = [POINTER(drmaa2_jsession), POINTER(drmaa2_jtemplate),
                                                             c_longlong, c_longlong, c_longlong, c_longlong]
        drmaa2_lib.drmaa2_jsession_wait_any_started.restype = POINTER(drmaa2_j)
        drmaa2_lib.drmaa2_jsession_wait_any_started.argtypes = [POINTER(drmaa2_jsession), drmaa2_j_list, drmaa2_time]
        drmaa2_lib.drmaa2_jsession_wait_any_terminated.restype = POINTER(drmaa2_j)
        drmaa2_lib.drmaa2_jsession_wait_any_terminated.argtypes = [POINTER(drmaa2_jsession), drmaa2_j_list, drmaa2_time]
        drmaa2_lib.drmaa2_jsession_wait_all_started.restype = drmaa2_j_list
        drmaa2_lib.drmaa2_jsession_wait_all_started.argtypes = [POINTER(drmaa2_jsession), drmaa2_j_list, drmaa2_time]
        drmaa2_lib.drmaa2_jsession_wait_all_terminated.restype = drmaa2_j_list
        drmaa2_lib.drmaa2_jsession_wait_all_terminated.argtypes = [POINTER(drmaa2_jsession), drmaa2_j_list, drmaa2_time]
        drmaa2_lib.drmaa2_j_suspend.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_suspend.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_suspend_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_suspend_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_resume.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_resume.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_resume_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_resume_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_hold.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_hold.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_hold_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_hold_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_release.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_release.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_release_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_release_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_terminate.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_terminate.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_terminate_forced.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_terminate_forced.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_terminate_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_terminate_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_j), drmaa2_bool]
        drmaa2_lib.drmaa2_j_terminate_all.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_terminate_all.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_terminate_forced_all.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_terminate_forced_all.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_terminate_all_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_terminate_all_as.argtypes = [POINTER(drmaa2_sudo), POINTER(drmaa2_j), drmaa2_bool]
        drmaa2_lib.drmaa2_j_reap.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_reap.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_get_id.restype = drmaa2_string
        drmaa2_lib.drmaa2_j_get_id.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_get_jtemplate.restype = POINTER(drmaa2_jtemplate)
        drmaa2_lib.drmaa2_j_get_jtemplate.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_get_state.restype = drmaa2_jstate
        drmaa2_lib.drmaa2_j_get_state.argtypes = [POINTER(drmaa2_j), POINTER(drmaa2_string)]
        drmaa2_lib.drmaa2_j_get_info.restype = POINTER(drmaa2_jinfo)
        drmaa2_lib.drmaa2_j_get_info.argtypes = [POINTER(drmaa2_j)]
        drmaa2_lib.drmaa2_j_wait_started.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_wait_started.argtypes = [POINTER(drmaa2_j), drmaa2_time]
        drmaa2_lib.drmaa2_j_wait_terminated.restype = drmaa2_error
        drmaa2_lib.drmaa2_j_wait_terminated.argtypes = [POINTER(drmaa2_j)]

        drmaa2_lib.drmaa2_msession_get_all_reservations.restype = drmaa2_r_list
        drmaa2_lib.drmaa2_msession_get_all_reservations.argtypes = [POINTER(drmaa2_msession)]

        drmaa2_lib.drmaa2_msession_get_all_jobs.restype = drmaa2_j_list
        drmaa2_lib.drmaa2_msession_get_all_jobs.argtypes = [POINTER(drmaa2_msession), POINTER(drmaa2_jinfo)]
        drmaa2_lib.drmaa2_msession_get_all_queues.restype = drmaa2_queueinfo_list
        drmaa2_lib.drmaa2_msession_get_all_queues.argtypes = [POINTER(drmaa2_msession), drmaa2_string_list]
        drmaa2_lib.drmaa2_msession_get_all_machines.restype = drmaa2_machineinfo_list
        drmaa2_lib.drmaa2_msession_get_all_machines.argtypes = [POINTER(drmaa2_msession), drmaa2_string_list]

        drmaa2_lib.drmaa2_get_drms_name.restype = drmaa2_string
        drmaa2_lib.drmaa2_get_drms_name.argtypes = []
        drmaa2_lib.drmaa2_get_drms_version.restype = POINTER(drmaa2_version)
        drmaa2_lib.drmaa2_get_drms_version.argtypes = []
        drmaa2_lib.drmaa2_get_drmaa_name.restype = drmaa2_string
        drmaa2_lib.drmaa2_get_drmaa_name.argtypes = []
        drmaa2_lib.drmaa2_get_drmaa_version.restype = POINTER(drmaa2_version)
        drmaa2_lib.drmaa2_get_drmaa_version.argtypes = []
        drmaa2_lib.drmaa2_supports.restype = drmaa2_bool
        drmaa2_lib.drmaa2_supports.argtypes = [drmaa2_capability]
        drmaa2_lib.drmaa2_create_jsession.restype = POINTER(drmaa2_jsession)
        drmaa2_lib.drmaa2_create_jsession.argtypes = [c_char_p, c_char_p]
        drmaa2_lib.drmaa2_create_jsession_as.restype = POINTER(drmaa2_jsession)
        drmaa2_lib.drmaa2_create_jsession_as.argtypes = [POINTER(drmaa2_sudo), c_char_p, c_char_p]
        drmaa2_lib.drmaa2_create_rsession.restype = POINTER(drmaa2_rsession)
        drmaa2_lib.drmaa2_create_rsession.argtypes = [c_char_p, c_char_p]
        drmaa2_lib.drmaa2_create_rsession_as.restype = POINTER(drmaa2_rsession)
        drmaa2_lib.drmaa2_create_rsession_as.argtypes = [POINTER(drmaa2_sudo), c_char_p, c_char_p]
        drmaa2_lib.drmaa2_open_jsession.restype = POINTER(drmaa2_jsession)
        drmaa2_lib.drmaa2_open_jsession.argtypes = [c_char_p]
        drmaa2_lib.drmaa2_open_rsession.restype = POINTER(drmaa2_rsession)
        drmaa2_lib.drmaa2_open_rsession.argtypes = [c_char_p]
        drmaa2_lib.drmaa2_open_msession.restype = POINTER(drmaa2_msession)
        drmaa2_lib.drmaa2_open_msession.argtypes = [c_char_p]
        drmaa2_lib.drmaa2_close_jsession.restype = drmaa2_error
        drmaa2_lib.drmaa2_close_jsession.argtypes = [POINTER(drmaa2_jsession)]
        drmaa2_lib.drmaa2_close_rsession.restype = drmaa2_error
        drmaa2_lib.drmaa2_close_rsession.argtypes = [POINTER(drmaa2_rsession)]
        drmaa2_lib.drmaa2_close_msession.restype = drmaa2_error
        drmaa2_lib.drmaa2_close_msession.argtypes = [POINTER(drmaa2_msession)]
        drmaa2_lib.drmaa2_destroy_jsession.restype = drmaa2_error
        drmaa2_lib.drmaa2_destroy_jsession.argtypes = [c_char_p]
        drmaa2_lib.drmaa2_destroy_jsession_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_destroy_jsession_as.argtypes = [POINTER(drmaa2_sudo), c_char_p]
        drmaa2_lib.drmaa2_destroy_rsession.restype = drmaa2_error
        drmaa2_lib.drmaa2_destroy_rsession.argtypes = [c_char_p]
        drmaa2_lib.drmaa2_destroy_rsession_as.restype = drmaa2_error
        drmaa2_lib.drmaa2_destroy_rsession_as.argtypes = [POINTER(drmaa2_sudo), c_char_p]
        drmaa2_lib.drmaa2_get_jsession_names.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_get_jsession_names.argtypes = []
        drmaa2_lib.drmaa2_get_rsession_names.restype = drmaa2_string_list
        drmaa2_lib.drmaa2_get_rsession_names.argtypes = []
        drmaa2_lib.drmaa2_register_event_notification.restype = drmaa2_error
        drmaa2_lib.drmaa2_register_event_notification.argtypes = [POINTER(drmaa2_callback)]
        cls.logger.debug("Done initializing DRMAA2 library")
        return drmaa2_lib


#######################################################################
# Test.
if __name__ == '__main__':
    lm = LibraryManager()
    print(lm.get_drmaa2_library())
