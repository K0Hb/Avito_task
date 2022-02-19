run :
	uvicorn app.handlers:app --reload

lint :
	poetry run flake8