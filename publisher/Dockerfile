FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install -r publisher/requirements.txt

CMD ["python", "-m", "publisher.app"]