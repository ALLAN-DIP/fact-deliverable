.PHONY: default
default:
	@echo "an explicit target is required"

SHELL=/usr/bin/env bash

export PYTHONPATH := $(shell realpath .)

.PHONY: lock
lock:
	# Complex logic needed to pin `setuptools` but not `pip` in Python 3.11 and earlier
	PYTHON_VERSION_AT_LEAST_3_12=$(shell python -c 'import sys; print(int(sys.version_info >= (3, 12)))')
ifeq ($(PYTHON_VERSION_AT_LEAST_3_12),1)
	pip freeze >requirements-lock.txt
else
	pip freeze --all --exclude pip >requirements-lock.txt
endif
	# Remove editable packages because they are expected to be available locally
	sed --in-place -e '/^-e .*/d' requirements-lock.txt
	# Strip local versions so PyTorch is the same on Linux and macOS
	sed --in-place -e 's/+[[:alnum:]]\+$$//g' requirements-lock.txt
	# Remove nvidia-* and triton because they cannot be installed on macOS
	# The packages have no sdists, and their wheels are not available for macOS
	# They install automatically on Linux as a requirement of PyTorch
	sed --in-place -e '/^\(nvidia-.*\|triton\)==.*/d' requirements-lock.txt

.PHONY: update
update:
	pip install --upgrade pip
	pip install --upgrade -r requirements-lock.txt -e .

.PHONY: upgrade
upgrade:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -r requirements.txt -e .

.PHONY: install
install:
	make update
