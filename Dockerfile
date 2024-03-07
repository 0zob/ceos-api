from python:3.11-alpine as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

from python:3.11-alpine

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/
COPY ./alembic* /code/

EXPOSE 80

CMD ["uvicorn", "ceos.main:app", "--host", "0.0.0.0", "--port", "80"]
