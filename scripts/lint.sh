#!/usr/bin/env bash

set -e
set -x

isort -c sqlalchemy_model_builder tests
pylint sqlalchemy_model_builder tests
mypy sqlalchemy_model_builder tests