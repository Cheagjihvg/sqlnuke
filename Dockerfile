FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y python3-venv python3-pip

# Set environment variables
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH

# Create the virtual environment
RUN python -m venv --copies /opt/venv

# Use pip from the venv and mount the cache correctly
RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app
