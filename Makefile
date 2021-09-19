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

.PHONY: ci
ci: lint test
