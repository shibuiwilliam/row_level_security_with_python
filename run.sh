#!/bin/bash

set -eu

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-1}
LOG_CONFIG=${LOG_CONFIG:-"./src/middleware/logging.yaml"}
LOG_LEVEL=${LOG_LEVEL:-"info"}
APP_NAME=${APP_NAME:-"src.main:app"}

uvicorn ${APP_NAME} \
  --host ${HOST} \
  --port ${PORT} \
  --workers ${WORKERS} \
  --log-config ${LOG_CONFIG} \
  --log-level ${LOG_LEVEL} \
  --reload
