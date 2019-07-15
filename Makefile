test: pyclean isort lint run-tests

pyclean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -type d -name "__pycache__" -delete

isort:
	isort --recursive --diff --check .

lint:
	flake8 .

run-tests:
	py.test

install-test:
	pip install -e .[test]
