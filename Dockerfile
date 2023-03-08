FROM python:3-alpine

RUN apk add --update python3 py3-pip
RUN apk add git
RUN apk add nmap
RUN apk add freetype-dev
RUN apk add gcc musl-dev curl-dev openssl-dev python3-dev

RUN pip install --upgrade pip

WORKDIR /usr/src/recon
COPY assets/ assets/
COPY modules/ modules/
COPY app.py .
COPY packages.list .
RUN pip3 install --no-cache-dir -r packages.list

CMD python3 app.py
