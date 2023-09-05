# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app


# Install poetry
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock /usr/src/app/

# Project initialization
RUN poetry config virtualenvs.create true && \
    poetry install --only main

# Copy all files
COPY . /usr/src/app

ENV PYTHONPATH='.'
ENV PYTHONUNBUFFERED=1
