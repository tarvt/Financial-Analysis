FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y openjdk-11-jdk

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

CMD ["python", "app.py"]
EXPOSE 6379
