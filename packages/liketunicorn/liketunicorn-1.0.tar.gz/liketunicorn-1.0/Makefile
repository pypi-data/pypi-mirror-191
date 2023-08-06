package_dir := src/liketunicorn
tests_dir := tests
code_dir = $(package_dir) $(tests_dir)

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -name .pytest_cache`
	rm -f .coverage
	rm -rf {dist,.cache,reports}

.PHONY: lint
lint:
	isort --check-only $(code_dir)
	black --check --diff $(code_dir)
	ruff $(package_dir)

.PHONY: reformat
reformat:
	black $(code_dir)
	isort $(code_dir)


.PHONY: tests
tests:
	PYTHONPATH=. pytest --cov=liketunicorn --cov-report html --cov-config .coveragerc tests/
