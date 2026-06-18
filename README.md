# url-shortener

Minimal URL shortener in Python using Flask.

## Run

    pip install -r requirements.txt
    gunicorn app:app

## Use

### Shorten a URL

    curl -X POST --data "https://example.com" http://127.0.0.1:8000/shorten

### Resolve

    curl --follow http://127.0.0.1:8000/r/BJePXN
