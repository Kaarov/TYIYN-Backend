# Tyiyn Finance Mobile Application

# Local development


## Initial requirements

With default configs project requires:
 - `postgres` running on default `5432` localhost port with
    `POSTGRES_PASSWORD=postgres_password` `POSTGRES_USER=postgres` for project itself.

Project uses `poetry` for dependency management:
```shell
cp .env.example .env
```

```shell
poetry install
```

## Running

Run server:
```shell
python manage.py runserver
```



# Production deployment

Project was dockerized with love and pain.

## Initial requirements

* docker
* docker compose

Tested on:
```shell
> docker --version
Docker version 23.0.1, build a5ee5b1
```

```shell
> docker-compose up
```
