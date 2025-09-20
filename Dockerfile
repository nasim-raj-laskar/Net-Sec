FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

# Install Python dependencies including AWS CLI
RUN pip install --no-cache-dir awscli
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]