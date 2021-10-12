.PHONY: setup
setup:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt

.PHONY: lint
lint:
	flake8 alarm tests

.PHONY: typing
typing:
	mypy alarm tests

.PHONY: test
test:
	tox

.PHONY: coverage
cov:
	pytest --cov=alarm --cov-report term-missing

.PHONY: ci
ci: lint test
