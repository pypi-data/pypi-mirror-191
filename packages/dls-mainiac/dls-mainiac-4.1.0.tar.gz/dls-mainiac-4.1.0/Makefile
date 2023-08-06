# This is needed so local copy of dependencies supercede the installed ones.
BASIC_PATH=src:../dls-logformatter/src
PYTHONPATH=$(BASIC_PATH)

# ------------------------------------------------------------------
# Tests individually.

test:
	PYTHONPATH=tests:$(PYTHONPATH) \
	python3 -m pytest -sv -ra --tb=line tests/$(t)

test-01-simple:
	PYTHONPATH=$(PYTHONPATH) python3 -m pytest -sv -ra --tb=line tests/test_01_simple.py

test-02-subcommand:
	PYTHONPATH=$(PYTHONPATH) python3 -m pytest -sv -ra --tb=line tests/test_02_subcommand.py
	
test-03-default_subcommand:
	PYTHONPATH=$(PYTHONPATH) python3 -m pytest -sv -ra --tb=line tests/test_03_default_subcommand.py
	
test-04-rotating:
	PYTHONPATH=$(PYTHONPATH) python3 -m pytest -sv -ra --tb=line tests/test_04_rotating.py
	
test-05-duplicate:
	PYTHONPATH=$(PYTHONPATH) python3 -m pytest -sv -ra --tb=line tests/test_05_duplicate.py
	
# ------------------------------------------------------------------
# These targets are hit by scisof-bxflow-templates/gitlab-ci-template.yml.
# The template provides environment variables:
# - PYTHON_VERSION
# - PIP_TARGET
# - SECRET_GITLAB_READ_REPOSITORY_TOKEN

pytest:
	PYTHONPATH=$(PYTHONPATH) pytest

install-dependency:
	pip install \
		--no-deps \
		--python-version $(PYTHON_VERSION) \
		--target $(PIP_TARGET) \
		--upgrade git+https://$(SECRET_GITLAB_READ_REPOSITORY_TOKEN)@gitlab.diamond.ac.uk/scisoft/bxflow/$(project).git && \
		rm -rf build

install-dependencies:
	make install-dependency project=dls-logformatter

# ------------------------------------------------------------------
# Utility.

tree:
	tree -I "__*" dls_mainiac_lib

	tree -I "__*" tests

.PHONY: list
list:
	@awk "/^[^\t:]+[:]/" Makefile | grep -v ".PHONY"

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -rf {} \;

show-version:
	PYTHONPATH=$(PYTHONPATH) python3 -m dls_mainiac_lib.version --json
	PYTHONPATH=$(PYTHONPATH) python3 -m dls_mainiac_lib.version

# ------------------------------------------------------------------
# Version bumping.  Configured in setup.cfg. 
# Thanks: https://pypi.org/project/bump2version/
bump-patch:
	bump2version --list patch

bump-minor:
	bump2version --list minor

bump-major:
	bump2version --list major
	
bump-dryrun:
	bump2version --dry-run patch
	