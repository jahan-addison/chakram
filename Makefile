
project = chakram

type:
	poetry run python -m mypy --ignore-missing-imports **/*.py

lint: type
	poetry run python -m flake8 --ignore E501,F841 $(project)/

test: lint
	poetry run pytest --cov-branch --cov=chakram --disable-warnings -s

run: lint
	# run the first example
	poetry run python $(shell pwd)/$(project)/__main__.py -f ./examples/1.b -p

requirements: lint
	poetry run pip freeze > requirements.txt

install: lint
	python -m pip install .