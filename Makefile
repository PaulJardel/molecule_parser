SRC_PATH=./molecular
TEST_PATH=./tests

lint:
	flake8 $(SRC_PATH) --max-line-length=120
	flake8 $(TEST_PATH) --max-line-length=150

test:
	pytest -s -vvv $(TEST_PATH)
