.PHONY: help clean clean-pyc clean-build list test test-all coverage docs release sdist

help:
	@echo "clean - remove all build/python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"

clean: clean-build clean-pyc

clean-build:
	rm -fr htmlcov/
	rm -fr build/
	rm -fr dist/
	rm -fr deb_dist/
	rm -fr *.egg-info
	rm -f *.tar.gz
	rm -f *.xml
	rm -f *.log
	rm -fr .tox
	find . -name '__pycache__' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
