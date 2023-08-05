FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y build-essential libssl-dev libffi-dev wget libegl1 libopengl0 \
    && wget -q -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin install_dir=/usr/local \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential libssl-dev libffi-dev wget \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/* \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "-u", "manga_watchdog.py", "--data-path", "/app/data", "--calibre-library-path", "/app/calibre"]