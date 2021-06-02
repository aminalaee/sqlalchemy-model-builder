#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint.sh

coverage run --source fastapi_admin -m pytest tests
coverage report --fail-under 95
coverage xml