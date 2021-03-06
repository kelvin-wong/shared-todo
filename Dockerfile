FROM python:3.9-slim-bullseye

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
COPY .env.dist /app/.env
RUN python3 -m venv .venv

ENV PATH=".venv/bin:${PATH}"
RUN poetry export -o requirements.txt --without-hashes && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
