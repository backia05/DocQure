# Dockerfile for scheduling-service
FROM python:3.9-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y postgresql-client
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY wait-for-db.sh .
COPY . .
RUN chmod +x wait-for-db.sh
EXPOSE 5003
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003
CMD ["./wait-for-db.sh", "postgres-db", "flask", "run"]