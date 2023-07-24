# Use the official Ubuntu LTS 22.04 as the base image
FROM ubuntu:22.04

# Update packages and install necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.10 and pip
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip

# Upgrade pip to the latest version
RUN python3.10 -m pip install --no-cache-dir --upgrade pip

ENV TZ=America/Sao_Paulo

WORKDIR /app

# Copy the requirements file to the working directory
COPY . .

# Install the Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# execute workers
ENTRYPOINT celery -A xai_tasks.app worker --loglevel=info


