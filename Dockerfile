FROM python:3.9.0a4-buster

WORKDIR /opt/pihome

COPY ["./application/", "./"]
RUN pip install -r requirements.txt

CMD python webapp.py
