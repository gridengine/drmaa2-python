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

BUILDDIR=build


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
ifdef SUBDIRS
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

GOALS=$(filter-out $(FILTER_GOALS),$(filter-out $(SUBDIRS),$(MAKECMDGOALS)))

.PHONY: all install deps clean distclean test

all:  recurse

install deps clean distclean test: recurse

.PHONY: recurse
recurse: $(SUBDIRS)

.PHONY: $(SUBDIRS)
$(SUBDIRS):
# Don't build anything if we goal was passed and all were filtered
ifneq ($(strip $(GOALS)),)
	$(MAKE) -C $@ $(GOALS)
else
# Check if no goal was passed... if so we build our default target
ifeq ($(strip $(MAKECMDGOALS)),)
	$(MAKE) -C $@ 
endif
endif
endif


#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
ifdef SUBMAKEFILES
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
.PHONY: all install deps clean distclean test

all: recurse

deps install clean distclean test: recurse

.PHONY: recurse
recurse: $(SUBMAKEFILES) $(SUBDIRS)

.PHONY: $(SUBMAKEFILES)
$(SUBMAKEFILES):
	$(MAKE) -f $@ $(MAKECMDGOALS)
endif
