
include ./util/include.mk

# The command line arguments of pandoc were renamed between version 1.x and 2.x,
# so find out which pandoc version we are using and set options accordingly.
PANDOC_EXISTS := $(shell pandoc -v 2>/dev/null)

ifdef PANDOC_EXISTS
PANDOC_VERSION_MAJOR = $(shell pandoc -v | grep "^pandoc" | cut -d" " -f 2 | cut -d"." -f 1)
PANDOC_VERSION_GE_2 = $(shell [ $(PANDOC_VERSION_MAJOR) -ge 2 ] && echo true)

ifeq ($(PANDOC_VERSION_GE_2),true)
	PANDOC_OPTS = --pdf-engine=xelatex
else
	PANDOC_OPTS = -R --latex-engine=xelatex
endif

endif

all: build doc

# Stubs for default targets
.PHONY:deps install clean dist egg wheel distclean test doc
deps install test:

drmaa2/__init__.py : ./util/params.mk
	cat $@ | sed 's?__version__ =.*?__version__ = $(VERSION)?' > $@.2 && mv $@.2 $@

distclean: tidy

build: dist

doc: 
	mkdir -p doc/source/_static
	PYTHONPATH=$(PWD) make -C doc html

pdf:
#	(cd doc/UserDocumentation; pandoc $(PANDOC_OPTS) --template=template.tex --listings -H listings.tex \
		--variable mainfont=Georgia --variable sansfont=Arial \
		--variable fontsize=10pt --variable version="$(REVISION)" \
		--variable title="Grid Engine Configuration API User Guide" \
		--variable author="Univa Engineering" --variable company="Univa Corporation" \
		--variable UGELongVersion="$(REVISION)" --variable UGEShortVersion="$(REVISION)" \
		--variable UGEFullName="Univa Grid Engine" --variable UGEShortName="Grid Engine" \
		--variable doc-family="Univa Grid Engine Documentation" \
		--toc -s UGEConfigLibraryDoc.md -o UGEConfigLibraryDoc.pdf)

dist: sdist wheel doc
	rsync -arvlP doc/build/* dist/doc/
	(cd dist; zip -r drmaa2-python.zip `ls -d *`)

egg: drmaa2/__init__.py
	python setup.py bdist_egg

sdist: drmaa2/__init__.py
	python setup.py sdist

wheel: drmaa2/__init__.py
	python setup.py bdist_wheel

test: drmaa2/__init__.py
	mkdir -p build
	python setup.py nosetests

clean:
	make -C doc clean
	rm -rf test/.coverage *.egg-info `find . -name '*.pyc' -o -name '__pycache__' -o -name 'build'`

tidy: clean
	rm -rf dist

