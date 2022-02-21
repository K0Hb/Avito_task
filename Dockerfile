FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /avito

COPY .  /avito

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction

EXPOSE 8000

CMD ["make", "docker"]
