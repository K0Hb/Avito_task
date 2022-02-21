FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /avito_task

WORKDIR /avito_task

COPY poetry.lock pyproject.toml /avito_task/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction

COPY .  /avito_task

EXPOSE 8000

CMD ["make", "run"]
