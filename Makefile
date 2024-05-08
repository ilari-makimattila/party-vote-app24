bootstrap:
	@poetry install

typecheck:
	@poetry run mypy .

lint:
	@poetry run ruff check .

check: lint typecheck

format:
	@poetry run ruff check --fix .

test:
	@poetry run pytest

watchtest:
	@poetry run ptw . --patterns '*.py,*.toml,*.html'
