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

import os
import logging
from .singleton import Singleton


class LogManager(Singleton):
    """ 
    Singleton class for managing library logging output. Log level 
    can be set either programatically, or via the DRMAA2_LOG_LEVEL 
    environment variable. Valid levels are the same as for the python 
    logging module: DEBUG, INFO, WARNING, ERROR, CRITICAL.
    """

    LOG_LEVEL_ENV_VAR = 'DRMAA2_LOG_LEVEL'
    LOG_LEVEL_MAP = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }
    LOG_MESSAGE_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d:  %(message)s'

    __instance = None

    def __init__(self):
        """
        Constructor. 

        >>> lm = LogManager()
        """
        if LogManager.__instance:
            return
        LogManager.__instance = self
        self.configure()

    def configure(self, level=None):
        """
        Confgure the log level. 

        :param level: Log level; if not provided, the DRMAA2_LOG_LEVEL environment variable will be used to set the level.
        :type level: str

        >>> LogManager.get_instance.configure('DEBUG')
        """
        level = level or os.environ.get(self.LOG_LEVEL_ENV_VAR)
        if level:
            log_level = self.LOG_LEVEL_MAP.get(level.upper(), logging.NOTSET)
            logging.basicConfig(level=log_level, format=self.LOG_MESSAGE_FORMAT)
        else:
            logging.basicConfig(format=self.LOG_MESSAGE_FORMAT)

    @classmethod
    def get_logger(cls, name=None):
        """ 
        Get logger with a given name.

        :param name: Logger name; if not provided, class name will be used.
        :type name: str

        :returns: Logger object.

        >>> logger = LogManager.get_logger('MyClass')
        """
        name = name or cls.__name__
        return logging.getLogger(name)
