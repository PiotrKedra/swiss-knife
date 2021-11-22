FROM python:3

ADD network_settings.txt /

CMD [ "python", "./scripts/server.py" ]