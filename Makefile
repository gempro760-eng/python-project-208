install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

lint:
	uv run ruff check .

test:
	uv run pytest

test-coverage:
	uv run coverage run -m pytest
	uv run coverage report --fail-under=80

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi