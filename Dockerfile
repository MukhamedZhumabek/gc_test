FROM python:3.10.14-alpine3.19
WORKDIR /server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /server