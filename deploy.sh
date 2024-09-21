#!/bin/sh
docker compose down
rm -f requirements.txt
echo Assuming pipfile.lock is up to date
pipenv requirements > requirements.txt
docker container rm -f recueil_container
docker image rm recueil-web
docker image prune -f
docker compose up
