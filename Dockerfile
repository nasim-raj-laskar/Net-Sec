FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

# Install AWS CLI via pip and Python dependencies
RUN apt-get update -y && \
    pip install awscli && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["python3", "app.py"]