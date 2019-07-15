test: pyclean isort lint run-tests black

pyclean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -type d -name "__pycache__" -delete

isort:
	isort --recursive --diff --check .

lint:
	flake8 .

black:
	black --check --exclude "migrations" .

run-tests:
	py.test

install-test:
	pip install -e .[test]
