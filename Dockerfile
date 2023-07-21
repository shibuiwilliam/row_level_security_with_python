ARG FROM_IMAGE=python:3.11.3-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=.

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r /${PROJECT_DIR}/requirements.txt

COPY ${LOCAL_DIR}/src/ /${PROJECT_DIR}/src/
COPY ${LOCAL_DIR}/run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
