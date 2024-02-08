FROM python:3.9-slim

LABEL MAINTAINER="Mauricio Alpuin"

ENV GROUP_ID=1000 \
    USER_ID=1000
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY . .

RUN addgroup --gid $GROUP_ID www
RUN adduser -u $USER_ID --gid $GROUP_ID flask_user --shell /bin/sh

USER flask_user

EXPOSE 5000

CMD [ "gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:create_app()"]