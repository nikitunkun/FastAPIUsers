FROM python:3.9

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

COPY requirements/requirements.txt .
RUN pip install --upgrade pip
RUN ["pip", "install", "-r", "requirements.txt"]

COPY . .
