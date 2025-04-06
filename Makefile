-include .env

.PHONY: install
## Install environment settings
install:
	cp .env.example .env

.PHONY: format
## Apply black & isort code formatting
format:
	cd src && poetry run black .
	cd src && poetry run isort .

.PHONY: format-check
## Check for correct code format
format-check:
	cd src && poetry run black --check .
	cd src && poetry run isort --check-only .

.PHONY: lint
## Check code using linters
lint:
	cd src && poetry run flake8 .

.PHONY: mypy
## Check code using mypy
mypy:
	cd src && poetry run mypy .

.PHONY: clean
## Deletes temporary coverage files and caches
clean:
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage

.PHONY: tests-unit
## Run unit tests
tests-unit:
	cd src && poetry run pytest --disable-warnings -v tests/unit

.PHONY: tests-integration
## Run integration tests
tests-integration:
	cd src && poetry run pytest --disable-warnings -v tests/integration

.PHONY: tests
## Run unit & integration tests
tests: tests-unit tests-integration

.PHONY: coverage
## Get code coverage report
coverage:
	cd src && poetry run coverage report -i --rcfile=setup.cfg
	cd src && poetry run coverage html --rcfile=setup.cfg
	@echo "HTML report generated at: htmlcov/index.html"

.PHONY: ci
## Run CI checks
ci: | format-check lint mypy clean tests coverage
