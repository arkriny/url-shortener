# url-shortener

Minimal URL shortener in Python using Flask.

## Run

    pip install -r requirements.txt
    gunicorn app:app

Or using Docker:

```sh
docker build -t url-shortener .
docker run -p 8000:8000 url-shortener
```

Or using Docker Compose:

```sh
docker compose up
```

## Use

### Shorten a URL

    curl -X POST --data "https://example.com" http://127.0.0.1:8000/shorten

### Resolve

    curl --follow http://127.0.0.1:8000/r/BJePXN
