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

class Singleton(object):
    """ Base class for singleton objects. """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None or cls != type(cls.__instance):
            instance = object.__new__(cls, *args, **kwargs)
            instance.__init__()
            cls.__instance = instance
        return cls.__instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """ 
        Get singleton instance.

        >>> s = Singleton.get_instance()
        """
        return cls.__new__(cls, *args, **kwargs)

    def __init__(self):
        if self.__instance is not None:
            return


#######################################################################
# Test.
if __name__ == '__main__':
    a = Singleton()
    print('A=%s' % a)
    b = Singleton()
    print('B=%s' % b)
    c = Singleton.get_instance()
    print('C=%s' % c)
