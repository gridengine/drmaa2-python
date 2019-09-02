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


import copy
import re
from ctypes import cast
from ctypes import c_void_p
from ctypes import pointer

from .drmaa2_constants import PY_STRING_TYPE
from .drmaa2_constants import PY_BYTES_TYPE
from .drmaa2_constants import ListType
from .byte_string import ByteString
from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_list_entryfree

from .log_manager import LogManager
from .library_manager import LibraryManager
from .exception_mapper import ExceptionMapper

from .drmaa2_object_descriptors import Drmaa2BoolDescriptor
from .drmaa2_object_descriptors import Drmaa2EnumDescriptor
from .drmaa2_object_descriptors import Drmaa2TimeDescriptor
from .drmaa2_object_descriptors import Drmaa2IntDescriptor
from .drmaa2_object_descriptors import Drmaa2LongDescriptor
from .drmaa2_object_descriptors import Drmaa2LongLongDescriptor
from .drmaa2_object_descriptors import Drmaa2FloatDescriptor
from .drmaa2_object_descriptors import Drmaa2CharBufferDescriptor
from .drmaa2_object_descriptors import Drmaa2StringDescriptor
from .drmaa2_object_descriptors import Drmaa2StringListDescriptor
from .drmaa2_object_descriptors import Drmaa2DictDescriptor
from .drmaa2_object_descriptors import Drmaa2ImplSpecDescriptor


class Drmaa2Object(object):
    """ Base class for all high-level objects. """

    BoolDescriptor = Drmaa2BoolDescriptor
    EnumDescriptor = Drmaa2EnumDescriptor
    TimeDescriptor = Drmaa2TimeDescriptor
    CharBufferDescriptor = Drmaa2CharBufferDescriptor
    StringDescriptor = Drmaa2StringDescriptor
    StringListDescriptor = Drmaa2StringListDescriptor
    DictDescriptor = Drmaa2DictDescriptor
    IntDescriptor = Drmaa2IntDescriptor
    LongDescriptor = Drmaa2LongDescriptor
    LongLongDescriptor = Drmaa2LongLongDescriptor
    FloatDescriptor = Drmaa2FloatDescriptor
    ImplSpecDescriptor = Drmaa2ImplSpecDescriptor

    logger = LogManager.get_instance().get_logger('Drmaa2Object')
    drmaa2_lib = None
    implementation_specific_keys = None
    implementation_specific_attrs = None
    attribute_names = None

    def __init__(self, struct=None):
        """ Constructor. """
        self._struct = struct
        self._dict = {}
        self._read_only = False

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def get_drmaa2_library(cls):
        if not cls.drmaa2_lib:
            cls.drmaa2_lib = LibraryManager.get_instance().get_drmaa2_library()
        return cls.drmaa2_lib

    @classmethod
    def scrub_dict(cls, d):
        """ Remove empty keys from the dictionary. """
        return {k: v for (k, v) in d.items() if v is not None}

    def get_impl_spec_key_value(self, key):
        """ Get value for an implementation specific key. """
        ctypes_string = self.drmaa2_lib.drmaa2_get_instance_value(cast(self._struct, c_void_p), key.encode())
        # ExceptionMapper.check_last_error_code()
        return self.to_py_string(ctypes_string)

    def set_impl_spec_key_value(self, key, value):
        """ Get value for an implementation specific key. """
        ExceptionMapper.check_status_code(
            self.drmaa2_lib.drmaa2_set_instance_value(cast(self._struct, c_void_p), key.encode(), value.encode()))

    def init_impl_spec_key_values(self):
        """ Initialize values for implementation specific keys. """
        for key in self.get_implementation_specific_keys():
            self.set_impl_spec_key_value(key, '')

    @classmethod
    def create_from_ctypes(cls, ctypes_struct):
        """ Convert ctypes struct to DRMAA2 object. """
        if ctypes_struct:
            obj = cls()
            obj._struct = ctypes_struct
            return obj
        else:
            return None

    @classmethod
    def create_from_dict(cls, d):
        """ 
        Create from dictionary. 
       
        :param d: Input dictionary.
        :type d: dict
        """
        if isinstance(d, cls):
            return d

        obj = cls()
        obj.from_dict(d)
        return obj

    def from_dict(self, d):
        """ 
        Set from dictionary. 
       
        :param d: Input dictionary.
        :type d: dict
        """
        if not d:
            return

        if not self._struct:
            self._dict.join(d)
            return

        for (key, value) in d.items():
            self.logger.debug('Setting {}={}'.format(key, str(value)))
            setattr(self, key, value)

    def to_dict(self):
        """ 
        Conversion to dictionary. 

        :returns: Dictionary representing object's structure.

        >>> v = Version.get_drms_version()
        >>> print(v.to_dict())
        {'implementation_specific': {}, 'major': '8', 'minor': '6.0'}
        """
        d = dict()
        if not self._struct:
            for (k, v) in self._dict.items():
                if v is not None:
                    d[k] = v
                    if type(v) == PY_STRING_TYPE:
                        pass
                    elif type(v) == PY_BYTES_TYPE:
                        try:
                            d[k] = v.decode()
                        except AttributeError:
                            pass
        else:
            attributes = self.get_attribute_names(self._struct)
            for attr_name in attributes:
                v = getattr(self, attr_name)
                if v is not None:
                    d[attr_name] = v
        return d

    @classmethod
    def get_attribute_names(cls, struct):
        if cls.attribute_names is None and struct is not None:
            attributes = [field[0] for field in struct.contents._fields_]
            cls.attribute_names = []
            for attr_name in sorted(attributes):
                # Convert aXY to a_XY
                attr_name2 = re.sub('([a-z])([A-Z]{2,})', r'\1_\2', attr_name)
                # Convert Xa to _Xa
                attr_name2 = re.sub('([A-Z][a-z]{1,})', r'_\1', attr_name2).lower()
                cls.attribute_names.append(attr_name2)
        return cls.attribute_names

    def __str__(self):
        """ Conversion to string. """
        return str(self.to_dict())

    def __repr__(self):
        """ Object representation. """
        return '%s(%s)' % (self.__class__.__name__, self.__str__())

    @classmethod
    def to_py_dict(cls, ctypes_dict):
        py_dict = dict()
        if ctypes_dict:
            drmaa2_lib = cls.get_drmaa2_library()
            ctypes_list = drmaa2_lib.drmaa2_dict_list(ctypes_dict)
            list_size = drmaa2_lib.drmaa2_list_size(ctypes_list)
            if list_size < 0:
                ExceptionMapper.check_last_error_code()
            for i in range(list_size):
                void_ptr = drmaa2_lib.drmaa2_list_get(ctypes_list, i)
                key_ptr = cast(void_ptr, drmaa2_string).value
                value_ptr = drmaa2_lib.drmaa2_dict_get(ctypes_dict, key_ptr)
                key = ByteString(key_ptr).decode()
                value = ByteString(value_ptr).decode()
                py_dict[key] = value
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_list)))
            drmaa2_lib.drmaa2_dict_free(pointer(c_void_p(ctypes_dict)))
        return py_dict

    @classmethod
    def to_py_string_list(cls, ctypes_list):
        py_list = list()
        if ctypes_list:
            drmaa2_lib = cls.get_drmaa2_library()
            list_size = drmaa2_lib.drmaa2_list_size(ctypes_list)
            if list_size < 0:
                ExceptionMapper.check_last_error_code()
            for i in range(list_size):
                void_ptr = drmaa2_lib.drmaa2_list_get(ctypes_list, i)
                value = ByteString(cast(void_ptr, drmaa2_string).value).decode()
                py_list.append(value)
            drmaa2_lib.drmaa2_list_free(pointer(c_void_p(ctypes_list)))
        return py_list

    @classmethod
    def to_py_string(cls, ctypes_string, free_original=False):
        py_string = ByteString(ctypes_string.value).decode()
        if free_original:
            cls.get_drmaa2_library().drmaa2_string_free(pointer(ctypes_string))
        if not py_string:
            py_string = None
        return py_string

    @classmethod
    def to_ctypes_string_list(cls, py_list):
        drmaa2_lib = cls.get_drmaa2_library()
        ctypes_list = drmaa2_lib.drmaa2_list_create(int(ListType.STRINGLIST), drmaa2_list_entryfree())
        value_list = [ByteString(v).encode() for v in py_list]
        for i in range(len(value_list)):
            v = value_list[i]
            ExceptionMapper.check_status_code(drmaa2_lib.drmaa2_list_add(ctypes_list, v))
        return ctypes_list

    @classmethod
    def get_implementation_specific_keys(cls):
        return cls.implementation_specific_keys


#######################################################################
# Test.
if __name__ == '__main__':
    o = Drmaa2Object()
