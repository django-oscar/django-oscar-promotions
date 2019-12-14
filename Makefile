test: lint run-tests

isort:
	isort -q -c --recursive --diff oscar_promotions tests setup.py
	flake8

run-tests:
	pytest
