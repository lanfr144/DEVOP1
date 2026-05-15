FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y cron at && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD service cron start && service atd start && python app.py