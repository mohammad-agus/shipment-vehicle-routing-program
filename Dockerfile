FROM python:3.11

WORKDIR /project

COPY . /project

RUN pip install -r requirements.txt

ENTRYPOINT [ "bash" ]