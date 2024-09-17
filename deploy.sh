#!/bin/sh
docker compose down
rm -f requirements.txt
rm -f Pipfile.lock
pipenv lock
pipenv requirements > requirements.txt
docker container rm -f recueil_container
docker image rm recueil-web
docker image prune -f
docker compose up
