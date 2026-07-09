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

# After including params.mk, ARCH and other variables should be set.
ifndef TOP
ROOT            = $(dir $(filter %include.mk,$(MAKEFILE_LIST)))
ROOT            := $(ROOT:%/util/=%)
ROOT            := $(ROOT:util/=.)
export TOP             := $(shell cd $(ROOT) >/dev/null 2>&1 && echo $$PWD)
endif

include $(TOP)/util/params.mk
include $(TOP)/util/platform.mk
