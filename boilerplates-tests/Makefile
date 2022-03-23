.PHONY: setup install clean test lint

default: test

setup:
	pip install -r requirements.txt

install:
	python setup.py install

clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@find . -type d -name '*.ropeproject' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -rf venv/
	@rm -f src/*.egg*
	@rm -f MANIFEST
	@rm -rf docs/build/
	@rm -f .coverage.*

test:
	@tox -- -s

lint:
	@tox -e lint

