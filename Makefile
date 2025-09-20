.PHONY: test

test:
	python -m coverage run --source src -m pytest --html=reports/pytest/index.html
	python -m coverage html -d reports/coverage