#!/bin/sh
rm -f requirements.txt
pipenv run pip freeze > requirements.txt
docker compose up
rm -f requirements.txt