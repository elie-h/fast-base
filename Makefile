.PHONY: dev

dev:
	poetry shell
	uvicorn --host=0.0.0.0 app.api:app --port 7998 --reload --log-level debug --no-access-log 

lint:
	poetry run ruff app
	poetry run black app --check

types:
	poetry run pyright app

test:
	export PYTHONPATH='.'
	poetry run pytest app

checks:
	make lint
	make types
	make test		
