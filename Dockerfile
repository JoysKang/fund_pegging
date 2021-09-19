FROM python:3.8-slim

COPY . /code

WORKDIR /code

RUN pip install -r requirements.txt \
    && rm -rf ~/.cache/* \
    && rm -rf /var/lib/apt/lists/*

CMD uvicorn app:app --host 0.0.0.0 --port 9000