ARG PORT=5000

FROM python:3.10.6-alpine3.16 AS alpine
WORKDIR /app

RUN apk add sqlite
RUN apk add python3-dev
RUN apk --no-cache add musl-dev linux-headers g++
RUN python3 -m venv venv
RUN source venv/bin/activate
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE ${PORT}
