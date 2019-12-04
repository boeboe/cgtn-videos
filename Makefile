RUNTEST2=python2 -m unittest discover -v -b 
RUNTEST3=python3 -m unittest -v -b
ALLMODULES=$(patsubst %.py, %, $(wildcard test_*.py))

.PHONY: tests_2 tests_3 build clean upload_testpypi upload_pypi

default: clean build
upload: upload_testpypi upload_pypi
tests: tests_2 tests_3

tests_2:
	${RUNTEST2} ${ALLMODULES}

tests_3:
	${RUNTEST3} ${ALLMODULES}

install:
	python2 setup.py install && python3 setup.py install

build:
	python2 setup.py sdist bdist_wheel && python3 setup.py sdist bdist_wheel

clean:
	rm -rf ./build ./dist ./*.egg-info ./*/__pycache__ ./*/*/__pycache__ ./*/*/*.pyc ./*/*.pyc

upload_testpypi:
	twine upload --repository testpypi dist/*

upload_pypi:
	twine upload --repository pypi dist/*
