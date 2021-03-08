FROM python:3.9.2-alpine3.12
WORKDIR /var/bot/
RUN apt-get update & pip install -r requirements.txt
ENTRYPOINT [ "python"]
CMD [  "src/main.py"  ]