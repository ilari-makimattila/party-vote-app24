FROM python:3.12-slim

RUN apt-get update && apt-get install -y nodejs npm --no-install-recommends && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN useradd -m -u 1000 python

WORKDIR /app

COPY . .

ENTRYPOINT ["poetry", "run", "fastapi", "run", "voting24/web/app.py", "--proxy-headers", "--port=80"]

RUN (cd ui && npm install)
USER python
RUN poetry install --no-root --only main
