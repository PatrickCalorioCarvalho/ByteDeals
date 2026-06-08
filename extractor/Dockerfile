FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install -r extractor/requirements.txt

CMD ["python", "-m", "extractor.app"]