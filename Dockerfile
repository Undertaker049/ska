FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y \
        gcc \
        inotify-tools \
        curl \
        dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-mark hold curl dos2unix

WORKDIR /app

RUN mkdir -p /app/db /app/files /app/staticfiles /app/static/vendor \
    && chmod -R 755 /app/staticfiles /app/static

COPY . .

RUN dos2unix .vendors || true

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh"]