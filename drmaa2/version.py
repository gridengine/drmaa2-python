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

from ctypes import POINTER
from ctypes import cast
from ctypes import c_void_p
from ctypes import pointer

from .byte_string import ByteString
from .drmaa2_ctypes import drmaa2_version
from .drmaa2_ctypes import drmaa2_dict
from .drmaa2_object import Drmaa2Object


class Version(Drmaa2Object):
    """ High-level DRMAA2 version class. """

    major = Drmaa2Object.StringDescriptor('major')
    """ Major version string (str). """
    minor = Drmaa2Object.StringDescriptor('minor')
    """ Minor version string (str). """
    implementation_specific = Drmaa2Object.ImplSpecDescriptor('implementationSpecific')
    """ Implementation specific dictionary ({str:str}). """

    def __init__(self, version):
        """ 
        Constructor. 

        :param version: Low-level drmaa2_version struct.
        :type version: drmaa2_version
        """
        Drmaa2Object.__init__(self)
        if isinstance(version, POINTER(drmaa2_version)):
            self._struct = POINTER(drmaa2_version)()
            self._struct.contents = drmaa2_version()
            if version:
                self.major = ByteString(getattr(version.contents, 'major').value).decode()
                self.minor = ByteString(getattr(version.contents, 'minor').value).decode()
                self.implementation_specific = self.get_implementation_specific_attrs()
            else:
                self.major = "-NA-"
                self.minor = "-NA-"
        elif isinstance(version, drmaa2_version):
            self._struct = POINTER(drmaa2_version)()
            self._struct.contents = version
        else:
            raise InvalidArgument('Invalid argument: %s' % str(version))
        self._read_only = True

    def __del__(self):
        pass

    @classmethod
    def get_implementation_specific_attrs(cls):
        """
        Retrieve dict of implementation-specific attrs.

        :returns: {str:str} dict of implementation-specific attrs.

        >>> print(Version.get_implementation_specific_attrs())
        ['uge_version_json':'xyz']
        """
        ctypes_version = cls.get_drmaa2_library().drmaa2_get_drmaa_version();
        if cls.implementation_specific_attrs is None:
            cls.implementation_specific_attrs = cls.to_py_dict(
                cls.get_drmaa2_library().uge_vi_impl_spec_get(ctypes_version))
        return cls.implementation_specific_attrs

    @classmethod
    def get_implementation_specific_keys(cls):
        """
        Retrieve list of implementation-specific keys.

        :returns: String list of implementation-specific keys.

        >>> print(Version.get_implementation_specific_keys())
        ['uge_version_json']
        """
        if cls.implementation_specific_keys is None:
            cls.implementation_specific_keys = cls.to_py_string_list(
                cls.get_drmaa2_library().drmaa2_version_impl_spec())
        return cls.implementation_specific_keys

    @classmethod
    def get_drms_version(cls):
        """
        Retrieve DRMS version.

        :returns: DRMS version object.

        >>> v = Version.get_drms_version()
        >>> print(v.major)
        8
        >>> print(v.minor)
        6.0
        """
        ctypes_version = cls.get_drmaa2_library().drmaa2_get_drms_version();
        py_version = Version(ctypes_version)
        cls.get_drmaa2_library().drmaa2_version_free(ctypes_version)
        return py_version

    @classmethod
    def get_drmaa_version(cls):
        """
        Retrieve DRMAA version.

        :returns: DRMAA version object.

        >>> v = Version.get_drmaa_version()
        >>> print(v.major)
        2
        >>> print(v.minor)
        0
        """
        ctypes_version = cls.get_drmaa2_library().drmaa2_get_drmaa_version();
        py_version = Version(ctypes_version)
        cls.get_drmaa2_library().drmaa2_version_free(ctypes_version)
        return py_version
