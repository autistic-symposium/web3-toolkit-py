.PHONY: default clean run install test version dist

default: run

clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info

run:
	python3 app.py

install:
	pip3 install -r requirements.txt

test:
	pytest -vvv

dist: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel

version: dist
	python3 setup.py --version
