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

import types
import datetime
from ctypes import cast

from .byte_string import ByteString

from .drmaa2_constants import UNSET_BOOL
from .drmaa2_constants import UNSET_NUM
from .drmaa2_constants import UNSET_ENUM
from .drmaa2_constants import POSIX_EPOCH
from .drmaa2_constants import PY_STRING_TYPE

from .drmaa2_constants import ListType
from .drmaa2_constants import Bool
from .drmaa2_constants import Time

from .drmaa2_exceptions import UnsupportedAttribute

from .drmaa2_ctypes import drmaa2_string
from .drmaa2_ctypes import drmaa2_list
from .drmaa2_ctypes import drmaa2_string_list
from .drmaa2_ctypes import drmaa2_list_entryfree
from .drmaa2_ctypes import drmaa2_dict_entryfree

from .log_manager import LogManager
from .library_manager import LibraryManager
from .exception_mapper import ExceptionMapper


class Drmaa2Descriptor(object):
    """ Base descriptor class for drmaa2_object fields. """

    drmaa2_lib = None

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_drmaa2_library(cls):
        if not cls.drmaa2_lib:
            cls.drmaa2_lib = LibraryManager.get_instance().get_drmaa2_library()
        return cls.drmaa2_lib

    @classmethod
    def get_contents(cls, obj):
        if obj._struct is not None:
            if hasattr(obj._struct, 'contents'):
                return obj._struct.contents
            else:
                return obj._struct
        else:
            return None

    @classmethod
    def can_read(cls, obj):
        if obj is not None and obj._struct is not None:
            return True
        return False

    @classmethod
    def can_write(cls, obj):
        if obj is not None and obj._struct is not None and not obj._read_only:
            return True
        return False


class Drmaa2BoolDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_bool fields. """

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        value = False
        if self.can_read(obj):
            value = getattr(obj._struct.contents, self.name)
        return Bool(value).name

    def __set__(self, obj, value):
        if not self.can_write(obj):
            return

        if value is not None:
            if type(value) == PY_STRING_TYPE:
                value = Bool[value].value
            elif value:
                value = int(Bool.TRUE)
            else:
                value = int(Bool.FALSE)
        else:
            value = UNSET_BOOL
        setattr(obj._struct.contents, self.name, value)
        obj._dict[self.name] = value


class Drmaa2EnumDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_enum fields. """

    def __init__(self, name, cls):
        Drmaa2Descriptor.__init__(self, name)
        self.cls = cls

    def __get__(self, obj, type=None):
        value = UNSET_ENUM
        if self.can_read(obj):
            value = getattr(obj._struct.contents, self.name)
        if value == UNSET_ENUM:
            return None
        return self.cls(value).name

    def __set__(self, obj, value):
        if not self.can_write(obj):
            return
        if value is not None:
            if type(value) == PY_STRING_TYPE:
                value = self.cls[value].value
        else:
            value = UNSET_ENUM
        setattr(obj._struct.contents, self.name, value)
        obj._dict[self.name] = value


class Drmaa2TimeDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_enum fields. """

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        value = int(Time.UNSET_TIME)
        if self.can_read(obj):
            value = getattr(obj._struct.contents, self.name)
        try:
            t = Time(value)
            if t == Time.UNSET_TIME:
                return None
            else:
                return t.name
        except ValueError:
            return datetime.datetime.utcfromtimestamp(value)
            # return datetime.datetime.fromtimestamp(value)

    def __set__(self, obj, value):
        if not self.can_write(obj):
            return
        if value is not None:
            if type(value) == PY_STRING_TYPE:
                value = int(Time[value])
            elif isinstance(value, datetime.datetime):
                value = int((value - POSIX_EPOCH).total_seconds())
            else:
                value = int(value)
        else:
            value = int(Time.UNSET_TIME)
        setattr(obj._struct.contents, self.name, value)
        obj._dict[self.name] = value


class Drmaa2NumericTypeDescriptor(Drmaa2Descriptor):
    """ A descriptor for numeric type fields. """

    def __init__(self, name, unset_value=UNSET_NUM):
        Drmaa2Descriptor.__init__(self, name)
        self.unset_value = unset_value

    def __get__(self, obj, type=None):
        value = self.unset_value
        if self.can_read(obj):
            value = getattr(obj._struct.contents, self.name)
        if value == self.unset_value:
            value = None
        return value

    def __set__(self, obj, value):
        if not self.can_write(obj):
            return
        value = value if value is not None else self.unset_value
        setattr(obj._struct.contents, self.name, value)
        obj._dict[self.name] = value


class Drmaa2IntDescriptor(Drmaa2NumericTypeDescriptor):
    """ A descriptor for int fields. """

    def __init__(self, name, unset_value=UNSET_NUM):
        Drmaa2NumericTypeDescriptor.__init__(self, name, unset_value)


class Drmaa2LongDescriptor(Drmaa2IntDescriptor):
    """ A descriptor for long fields. """

    def __init__(self, name, unset_value=UNSET_NUM):
        Drmaa2IntDescriptor.__init__(self, name, unset_value)


class Drmaa2LongLongDescriptor(Drmaa2IntDescriptor):
    """ A descriptor for long long fields. """

    def __init__(self, name, unset_value=UNSET_NUM):
        Drmaa2IntDescriptor.__init__(self, name, unset_value)


class Drmaa2FloatDescriptor(Drmaa2NumericTypeDescriptor):
    """ A descriptor for float fields. """

    def __init__(self, name, unset_value=UNSET_NUM):
        Drmaa2NumericTypeDescriptor.__init__(self, name, unset_value)


class Drmaa2CharBufferDescriptor(Drmaa2Descriptor):
    """ A descriptor for char[] fields. """

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        value = None
        if self.can_read(obj):
            value = getattr(obj._struct.contents, self.name)
            if hasattr(value, 'value'):
                value = value.value
        return ByteString(value).decode()

    def __set__(self, obj, value):
        if not self.can_write(obj):
            return
        if value is None:
            return
        value = ByteString(value).encode()
        setattr(obj._struct.contents, self.name, value)
        obj._dict[self.name] = value


class Drmaa2StringDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_string fields. """

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        value = None
        if self.can_read(obj):
            value = getattr(obj._struct.contents, self.name)
            if hasattr(value, 'value'):
                value = value.value
        return ByteString(value).decode()

    def __set__(self, obj, value):
        if not self.can_write(obj):
            return
        if value is not None:
            value = ByteString(value).encode()
        else:
            value = ByteString(drmaa2_string()).encode()
        setattr(obj._struct.contents, self.name, value)
        obj._dict[self.name] = value


class Drmaa2StringListDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_string_list fields. """

    logger = LogManager.get_instance().get_logger('Drmaa2StringListDescriptor')

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        if not self.can_read(obj):
            return None
        value_list = list()
        ctypes_list = getattr(obj._struct.contents, self.name)
        if ctypes_list:
            count = self.get_drmaa2_library().drmaa2_list_size(ctypes_list)
            self.logger.debug('Converting ctypes list {} of size {}'.format(self.name, count))
            for i in range(count):
                void_ptr = self.get_drmaa2_library().drmaa2_list_get(ctypes_list, i)
                if void_ptr:
                    value = ByteString(cast(void_ptr, drmaa2_string).value).decode()
                    self.logger.debug('{}[{}] = {}'.format(self.name, i, value))
                    value_list.append(value)
                else:
                    ExceptionMapper.check_last_error_code()
                    value_list.append(None)
        return value_list

    def __set__(self, obj, value_list):
        if not self.can_write(obj):
            return
        if value_list is None:
            value_list = []
        ctypes_list = getattr(obj._struct.contents, self.name)
        if ctypes_list:
            count = self.get_drmaa2_library().drmaa2_list_size(ctypes_list)
            self.logger.debug('Clearing string list {} (size {})'.format(self.name, count))
            while count > 0:
                ExceptionMapper.check_status_code(self.get_drmaa2_library().drmaa2_list_del(ctypes_list, 0))
                count = self.get_drmaa2_library().drmaa2_list_size(ctypes_list)
        else:
            self.logger.debug('Creating string list {}'.format(self.name))
            ctypes_list = self.get_drmaa2_library().drmaa2_list_create(int(ListType.STRINGLIST),
                                                                       drmaa2_list_entryfree())
            setattr(obj._struct.contents, self.name, ctypes_list)

        value_list = [ByteString(v).encode() for v in value_list]
        for i in range(len(value_list)):
            v = value_list[i]
            self.logger.debug('Adding {}[{}] = {}'.format(self.name, i, v))
            ExceptionMapper.check_status_code(self.get_drmaa2_library().drmaa2_list_add(ctypes_list, v))
        # this assures proper memory management in python 3
        obj._dict[self.name] = value_list


class Drmaa2DictDescriptor(Drmaa2Descriptor):
    """ A descriptor for drmaa2_dict fields. """

    logger = LogManager.get_instance().get_logger('Drmaa2DictDescriptor')

    def __init__(self, name):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        if not self.can_read(obj):
            return None
        value_dict = dict()
        ctypes_dict = getattr(obj._struct.contents, self.name)
        if ctypes_dict:
            key_list = self.get_drmaa2_library().drmaa2_dict_list(ctypes_dict)
            if key_list:
                count = self.get_drmaa2_library().drmaa2_list_size(key_list)
                for i in range(count):
                    void_ptr = self.get_drmaa2_library().drmaa2_list_get(key_list, i)
                    key = cast(void_ptr, drmaa2_string).value
                    value = self.get_drmaa2_library().drmaa2_dict_get(ctypes_dict, key)
                    key = ByteString(key).decode()
                    value = ByteString(value).decode()
                    self.logger.debug('{}[{}] = {}'.format(self.name, key, value))
                    value_dict[key] = value
                self.logger.debug('Clearing key list for dict {}'.format(self.name))
                self.get_drmaa2_library().drmaa2_list_free(cast(key_list, drmaa2_string_list))
        return value_dict

    def __set__(self, obj, value_dict):
        if not self.can_write(obj):
            return
        if value_dict is None:
            value_dict = {}
        ctypes_dict = getattr(obj._struct.contents, self.name)
        if ctypes_dict:
            key_list = self.get_drmaa2_library().drmaa2_dict_list(ctypes_dict)
            if key_list:
                count = self.get_drmaa2_library().drmaa2_list_size(key_list)
                self.logger.debug('Clearing dict {} (size {})'.format(self.name, count))
                for i in range(count):
                    void_ptr = self.get_drmaa2_library().drmaa2_list_get(key_list, i)
                    key = cast(void_ptr, drmaa2_string).value
                    ExceptionMapper.check_status_code(self.get_drmaa2_library().drmaa2_dict_del(ctypes_dict, key))
        else:
            self.logger.debug('Creating dict {}'.format(self.name))
            ctypes_dict = self.get_drmaa2_library().drmaa2_dict_create(drmaa2_dict_entryfree())
            setattr(obj._struct.contents, self.name, ctypes_dict)

        value_dict = {ByteString(k).encode(): ByteString(v).encode() for (k, v) in value_dict.items()}
        for (k, v) in value_dict.items():
            self.logger.debug('{}[{}] = {}'.format(self.name, k, v))
            ExceptionMapper.check_status_code(self.get_drmaa2_library().drmaa2_dict_set(ctypes_dict, k, v))
        # this assures proper memory management in python 3
        obj._dict[self.name] = value_dict


class Drmaa2ImplSpecDescriptor(Drmaa2Descriptor):
    """ A descriptor for implementation specific fields. """

    logger = LogManager.get_instance().get_logger('Drmaa2ImplSpecDescriptor')

    def __init__(self, name='implementationSpecific'):
        Drmaa2Descriptor.__init__(self, name)

    def __get__(self, obj, type=None):
        if not self.can_read(obj):
            return None
        implSpecDict = {}
        for key in obj.get_implementation_specific_keys():
            try:
                value = obj.get_impl_spec_key_value(key)
            except UnsupportedAttribute as ex:
                # Okay, attribute was not set.
                value = None
            if value is not None:
                implSpecDict[key] = value
        return implSpecDict

    def __set__(self, obj, implSpecDict):
        if not self.can_write(obj):
            return
        for key in obj.get_implementation_specific_keys():
            value = implSpecDict.get(key)
            if value is not None:
                obj.set_impl_spec_key_value(key, value)


#######################################################################
# Test.
if __name__ == '__main__':
    o = Drmaa2BoolDescriptor('boolField')
