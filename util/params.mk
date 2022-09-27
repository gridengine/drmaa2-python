# ___INFO__MARK_BEGIN__
#######################################################################################
# Copyright 2008-2022 Altair Engineering Inc.
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
#
ifndef TOP
ROOT            = $(dir $(filter %params.mk,$(MAKEFILE_LIST)))
ROOT            := $(ROOT:%/util/=%)
ROOT            := $(ROOT:util/=.)
export TOP      := $(shell cd $(ROOT) >/dev/null 2>&1 && echo $$PWD)
endif

export DRMAA2_REL_STR    = Development
#export GIT_REV          := git$(shell git rev-parse --verify head)

# Setting the system environment variable DRMAA2_REL when running make
# will override the contents of the release string.
#
# ie:
#
# $ DRMAA2_REL="UGE DRMAA2 v1.0" make
#
# By default the file will contain the value of the DRMAA2_REL_STR makefile 
# variable bellow.
ifneq ($(strip $(GIT_REV)),)
export DRMAA2_REL_STR       = Development version ($(GIT_REV))
endif
export VERSION              = 8.8.0a0
export DRMAA2_PACKAGE_NAME  = drmaa2

