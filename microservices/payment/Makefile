install:
	poetry install

update:
	poetry update

reformat:
	poetry run black --line-length 120 src tests
	poetry run isort src tests

lint:
	poetry run flake8

test:
	poetry run pytest

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report -m
	poetry run coverage xml
