FROM python:3.11.10-bookworm
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    build-essential \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry

WORKDIR /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

COPY . /app

ENV PYTHON_GET_PIP_URL=
ENV PYTHON_GET_PIP_SHA256=
ENV PYTHON_SERVICE_ENV=prod

# 服务器开放端口
EXPOSE 8080

CMD poetry run python3 main.py
