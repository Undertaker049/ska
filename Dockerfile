FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir -p /app/db /app/files /app/staticfiles /app/static \
    && chmod -R 755 /app/staticfiles /app/static

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]