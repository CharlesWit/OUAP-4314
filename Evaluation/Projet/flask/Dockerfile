FROM python:3

RUN mkdir /home/flask
WORKDIR /home/flask

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "run.py"]
