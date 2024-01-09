FROM python:3.7-slim-buster

WORKDIR /app
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY project/ .

CMD ["uwsgi", "--ini", "uwsgi.ini"]
EXPOSE 5000
