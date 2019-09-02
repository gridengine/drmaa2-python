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

import string
import random
import os
import os.path
from tempfile import NamedTemporaryFile

from nose import SkipTest
from nose.tools import make_decorator

DEFAULT_RANDOM_STRING_LENGTH = 6
DEFAULT_RANDOM_INT_MIN = 0
DEFAULT_RANDOM_INT_MAX = 65536


def generate_random_string(size=DEFAULT_RANDOM_STRING_LENGTH,
                           chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_random_string_list(n_strings, string_length, delimiter=',', string_prefix=''):
    string_list = ''
    string_delimiter = ''
    for i in range(0, n_strings):
        string_list = '%s%s%s%s' % (string_list, string_delimiter,
                                    string_prefix,
                                    generate_random_string(string_length))
        string_delimiter = delimiter
    return string_list


def generate_random_int(lower_bound=DEFAULT_RANDOM_INT_MIN, upper_bound=DEFAULT_RANDOM_INT_MAX):
    return int(random.uniform(lower_bound, upper_bound + 1))


def generate_random_string_list(n_strings, string_length, delimiter=',', string_prefix=''):
    string_list = ''


# Common decorators
def needs_uge(func):
    def inner(*args, **kwargs):
        from drmaa2 import Drmaa2Exception
        if not os.environ.get('SGE_ROOT'):
            raise Drmaa2Exception('SGE_ROOT is not defined.')
        return func(*args, **kwargs)

    return make_decorator(func)(inner)


#############################################################################
# Testing
if __name__ == '__main__':
    pass
