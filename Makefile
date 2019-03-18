.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

init:
	pipenv install

init-dev:
	pipenv install -d

lock-requirements:
	pipenv lock -r > requirements.txt

run-test:
	pipenv run pytest --flake8 --black --cov=pubsub_split --cov-report term-missing tests/

release-test: clean
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release-prod: clean
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*

test: init-dev run-test
t: run-test
