FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

# Update package list and install awscli
RUN apt-get update -y && apt-get install -y awscli

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "app.py"]
