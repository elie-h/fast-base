.PHONY: dev
dev:
	poetry shell
	uvicorn --host=0.0.0.0 app.main:app --port 7999 --reload --log-level debug --no-access-log 

checks:
	