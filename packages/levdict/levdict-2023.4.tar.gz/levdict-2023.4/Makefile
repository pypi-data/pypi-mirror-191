ifndef VIRTUAL_ENV
$(error The Virtual Environment is not active!)
endif

MODULE=levdict

define HELP
Available commands are:\n
\ttest\t\tTests the source files with 'unittest' module\n
\tbuild\t\tBuilds a new version (remember to update version in toml)\n
\tupload\t\tUploads the new version to PiPy\n
\ttest_upload\tUploads the new version to Test PiPy\n
\ttest_install\tInstalls from Test PiPy\n
\tinstall\t\tInstalls from PiPy\n
endef
export HELP

SOURCES = $(wildcard ./src/$(MODULE)/*.py)
DISTROS = $(wildcard ./dist/*)

.PHONY: update
.PHONY: build
.PHONY: test_upload
.PHONY: test_install
.PHONY: upload
.PHONY: install
.PHONY: dev_install
.PHONY: help
.PHONY: test

update:
	python -m pip install --upgrade pip
	python -m pip install --upgrade build
	python -m pip install --upgrade twine

build:
	rm -f dist/*
	python -m build

test_upload:
	python -m twine upload --repository testpypi dist/*

test_install:
	python -m pip install -i https://test.pypi.org/project/ $(MODULE)

upload:
	python -m twine upload dist/*

install:
	python -m pip install $(MODULE)

dev_install:
	python -m pip install --editable .

test:
	python -m unittest

help:
	@echo $$HELP
