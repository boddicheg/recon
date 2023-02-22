FROM python:3-alpine

RUN apk add --update python3 py3-pip
RUN apk add git
RUN apk add nmap
RUN apk add freetype-dev

RUN pip install sqlmap
RUN pip install wfuzz
RUN pip install wafw00f

CMD python3 -m http.server 8079
