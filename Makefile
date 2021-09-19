.PHONY: setup
setup:
	poetry install

.PHONY: lint
lint:
	poetry run flake8 --exclude venv

.PHONY: typing
typing:
	poetry run mypy alarm tests

.PHONY: test
test:
	poetry run pytest

.PHONY: coverage
coverage:
	poetry run pytest --cov=alarm --cov-report term-missing

.PHONY: ci
ci: lint test
