bootstrap:
	@poetry install
	@(cd ui && npm install)

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

dev:
	@poetry run fastapi dev voting24/web/app.py
