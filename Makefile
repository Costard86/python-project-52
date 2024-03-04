install:
	poetry install

setup:
	make install
	sh ./build.sh

lint:
	poetry run flake8

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: test
test:
	poetry run coverage run --source='.' manage.py test

.PHONY: test-coverage
test-coverage:
	poetry run coverage xml

.PHONY: install test lint selfcheck check build
