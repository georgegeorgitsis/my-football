FROM python:latest
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
