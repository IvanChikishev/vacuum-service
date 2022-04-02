ARG PYTHON_VERSION=3.9-slim-buster

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  libpq-dev\
  libssl-dev \
  libffi-dev \
  libatlas-base-dev \
  cargo \
  rustc \
  gcc \
  libssl-dev \
  python3-dev \
  libjpeg62 \
  musl-dev \
  zlib1g-dev\
  libjpeg-dev \
  openssl

RUN apt install -y git
RUN pip install --upgrade pip
RUN pip install cryptography
RUN pip install flask
RUN pip install git+https://github.com/IvanChikishev/miio-vaccum-1c.git@main
COPY main.py .

CMD ["python", "main.py"]