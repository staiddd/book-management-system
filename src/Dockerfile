FROM python:3.10-slim-bullseye

WORKDIR /app

# Copy dependency files
COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080