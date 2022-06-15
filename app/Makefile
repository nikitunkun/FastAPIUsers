lint:
	pip install -r requirements/dev-requirements.txt
	flake8 src
	pylint src
	black --check --config black.toml src

format:
	pip install -r requirements/dev-requirements.txt
	black --verbose --config black.toml src alembic
	isort isort src/**/*.py

test:
	pip install -r requirements/test-requirements.txt
	pytest