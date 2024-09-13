#!/bin/sh
rm -f requirements.txt
pipenv run pip freeze > requirements.txt
docker build -t recueil:latest .