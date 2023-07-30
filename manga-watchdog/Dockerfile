FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache build-base libffi-dev openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base libffi-dev openssl-dev

COPY . .

CMD ["sh", "-c", "python app.py --data-path /app/data --calibre-library-path /app/calibre"]