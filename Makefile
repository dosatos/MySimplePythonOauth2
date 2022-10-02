CODE_DIR = ./src
TEST_DIR = ./test
RUN_TESTS = PYTHONPATH=$(CODE_DIR):$(TEST_DIR) poetry run pytest --verbosity=2 --showlocals --strict-markers

build: tests lint format

itests:
	$(RUN_TESTS) ./integ_tests

tests:
	$(RUN_TESTS) ./test


lint:
	poetry run flake8 --jobs 4 --statistics --show-source $(CODE_DIR) $(TEST_DIR) $(EXAMPLE_DIR)
	poetry run pylint --jobs 4 --rcfile=.pylintrc --recursive=y $(CODE_DIR) $(EXAMPLE_DIR)
	poetry run mypy $(CODE_DIR)
	poetry run black --target-version py36 --skip-string-normalization --check $(CODE_DIR) $(TEST_DIR) $(EXAMPLE_DIR)

format:
	poetry run black --target-version py36 --skip-string-normalization $(CODE_DIR) $(TEST_DIR) $(EXAMPLE_DIR)
	poetry run unify --in-place --recursive $(CODE_DIR) $(TEST_DIR) $(EXAMPLE_DIR)
