FROM python:3.9.0a4-buster

WORKDIR /opt/pihome

RUN apt update && apt install -y nmap
COPY ["./application/", "./"]
RUN pip install -r requirements.txt

CMD python webapp.py
