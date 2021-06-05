#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint.sh

coverage run --source sqlalchemy_model_builder -m pytest tests
coverage report --fail-under 90
coverage xml
