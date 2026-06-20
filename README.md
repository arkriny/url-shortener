# url-shortener

Minimal URL shortener in Python using Flask and Redis.

## Run

Requires Redis instance at $REDIS_HOST (defaults to localhost).

    pip install -r requirements.txt
    gunicorn app:app

Or using Docker:

    docker build -t url-shortener .
    docker run -p 8000:8000 url-shortener

Alternatively, full service configuration is provided in compose.yaml file.
Note that commands below require the 'url-shortener' image to exist locally.

Run using Docker Compose:

    docker compose up

Or using Docker Swarm:

    docker swarm init
    docker stack deploy -c compose.yaml url-shortener

## Use

### Register

    curl -X POST --data 'username=user&password=secret' http://127.0.0.1:8000/register

### Shorten a URL

    curl -X POST --data "https://example.com" http://user:secret@127.0.0.1:8000/urls

### Resolve

    curl --follow http://127.0.0.1:8000/r/BJePXN

### List user's URLs

    curl http://user:secret@127.0.0.1:8000/urls

### Update URL by code

    curl -X PUT --data "https://newexample.com" http://user:secret@127.0.0.1:8000/urls/BJePXN

### Delete URL by code

    curl -X DELETE http://user:secret@127.0.0.1:8000/urls/BJePXN
