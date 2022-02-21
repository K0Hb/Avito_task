run :
	uvicorn app.handlers:app --reload

lint :
	poetry run flake8

coverage:
	poetry run pytest --cov=app --cov-report=xml