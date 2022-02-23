run :
	uvicorn app.handlers:app --reload

lint :
	poetry run flake8

coverage:
	poetry run pytest --cov=app --cov-report=xml

create_base:
	yoyo apply --database postgresql://scott:tiger@localhost/db ./migrations

install : 
	poetry install

crate_table :
	yoyo apply --database mysql://root:22081991@localhost/Avito ./migrations

docker :
	meke crate_table
	make coverage

