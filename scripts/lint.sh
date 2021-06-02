#!/usr/bin/env bash

set -e
set -x

isort -c fastapi_admin tests
pylint fastapi_admin tests
mypy fastapi_admin tests