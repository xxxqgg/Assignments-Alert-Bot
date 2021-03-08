FROM python:3.8-buster
WORKDIR /var/bot/
COPY ./requirements.txt /tmp/requirements.txt
RUN apt-get update & apt-get install libssl-dev libffi-dev 
RUN pip --version  & pip install -r /tmp/requirements.txt
#ENTRYPOINT [ "python"]
CMD [ "python", "src/main.py"  ]
