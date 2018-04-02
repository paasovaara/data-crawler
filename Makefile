.PHONY: init clean test

init:
	pip3 install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -fr dist/

test:
	clean
	py.test --verbose --color=yes test

run-import:
	python3 ./importer/main.py
    
