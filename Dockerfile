# Dockerfile
FROM python:3.12-slim as python-base

# Python build stage
FROM python-base as builder

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install Node.js and npm (required for Tailwind)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Export dependencies to requirements.txt
RUN $HOME/.local/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes

# Final stage
FROM python-base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements from builder
COPY --from=builder /app/requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Install Tailwind dependencies and build
RUN python manage.py tailwind install
RUN python manage.py tailwind build

# Create directory for static files
RUN mkdir -p /app/staticfiles /app/media

# Run collectstatic
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "datalabs.wsgi:application", "--bind", "0.0.0.0:8000"]