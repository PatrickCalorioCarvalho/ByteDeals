FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install -r agentIA/requirements.txt

CMD ["python", "-m", "agentIA.app"]