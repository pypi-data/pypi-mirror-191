.PHONY: all
all:


.PHONY: update_requirements
update_requirements:
	rm -f requirements.txt requirements-dev.txt
	pip-compile --generate-hashes --no-header -o requirements.txt pyproject.toml
	pip-compile --generate-hashes --no-header --extra dev -o requirements-dev.txt pyproject.toml

.PHONY: format
format:
	isort ebc/
	black ebc/
	flake8 ebc/
	mypy ebc/

.PHONY: check
check:
	# safety check
	black --check ebc/
	flake8 ebc/
	mypy ebc/
	bandit -ll -r ebc

.PHONY: build
build:
	python -m build