#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# -----------------------------------------------------------------------------
# DOCKERFILE: WEB BACKEND SERVICE
# -----------------------------------------------------------------------------
# This Dockerfile configures the environment for the Python Flask backend service.
# It installs system scheduling utilities (cron and at) and runs Flask.
# -----------------------------------------------------------------------------

# Use Python 3.11 slim base image for a small, optimized container footprint
FROM python:3.11-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Update packages and install system services: cron (recurring tasks) and at (one-shot tasks)
# Clean package list afterwards to minimize image size
RUN apt-get update && apt-get install -y cron at && rm -rf /var/lib/apt/lists/*

# Copy python dependencies file first to utilize Docker build layer caching
COPY requirements.txt .

# Install dependencies without caching pip packages to keep the build light
RUN pip install --no-cache-dir -r requirements.txt

# Copy all local project files into the container working directory
COPY . .

# Expose port 5000 to the container network for Flask routing
EXPOSE 5000

CMD printf "7,37 * * * * /usr/local/bin/python /app/XAU/get_gold_price.py >> /app/logs/xau_cron.log 2>&1\n10,40 * * * * /usr/local/bin/python /app/XAU/load_xau.py >> /app/logs/xau_cron.log 2>&1\n" | crontab - && service cron start && service atd start && python app.py