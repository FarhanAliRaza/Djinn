#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m djinn.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec poetry run daphne djinn.project.asgi:application -p 8000 -b 0.0.0.0