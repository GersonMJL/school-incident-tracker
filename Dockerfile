# Use an official Python runtime as a parent image
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency management files
COPY poetry.lock pyproject.toml /app/

# Install Python dependencies
RUN poetry install --no-ansi

# Copy application code
COPY ./app .

# Expose port 8000 for the Django app
EXPOSE 8000

# Use a non-root user for security (optional)
RUN useradd -m appuser
USER appuser

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
