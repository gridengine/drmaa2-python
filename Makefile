
include ./util/include.mk

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

dist: egg wheel doc
	rsync -arvlP doc/build/* dist/doc/
	(cd dist; zip -r drmaa2-python.zip `ls -d *`)

egg: drmaa2/__init__.py
	python setup.py bdist_egg

wheel: drmaa2/__init__.py
	python setup.py bdist_wheel

test: drmaa2/__init__.py
	mkdir -p build
	python setup.py nosetests

clean:
	make -C doc clean
	rm -rf  dist test/.coverage *.egg-info `find . -name '*.pyc' -o -name '__pycache__' -o -name 'build'` 

tidy: clean
	rm -rf dist

