FROM python:3.9-slim-bullseye

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN python3 -m venv .venv

ENV PATH=".venv/bin:${PATH}"
RUN poetry export -o requirements.txt --without-hashes && \
    .venv/bin/pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
