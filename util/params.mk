# ___INFO__MARK_BEGIN__
#############################################################################
#
# This material contains trade secrets or otherwise confidential information
# owned by Siemens Industry Software Inc. or its affiliates (collectively,
# "Siemens"), or its licensors. Access to and use of this information is
# strictly limited as set forth in the Customer's applicable agreements with
# Siemens.
# Unpublished work. © 2026 Siemens.
#
#############################################################################
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
export VERSION              = 8.13.0a0
export DRMAA2_PACKAGE_NAME  = drmaa2
