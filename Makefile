.PHONY: test format lint check install clean

install:
	uv pip install -r requirements.txt

format:
	black tests
	isort tests

lint:
	flake8 src tests
	mypy src

check: format lint

test:
	python -m coverage run --source src -m pytest --html=reports/pytest/index.html
	python -m coverage html -d reports/coverage

clean:
	rm -rf reports/
	rm -rf .coverage
	rm -rf .pytest_cache/

all: install check test