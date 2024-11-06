FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apk update
RUN apk --no-cache add curl

COPY . .

CMD [ "python3", "server.py"]