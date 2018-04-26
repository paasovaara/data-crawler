.PHONY: init clean test

init:
	pip3 install pipenv
	pipenv install --dev

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -fr dist/

test:
	clean
	py.test --verbose --color=yes test

run-import:
	pipenv run python3 ./importer/main.py import

run-process:
	pipenv run python3 ./importer/main.py process
