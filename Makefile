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

.PHONY: install test lint selfcheck check build
