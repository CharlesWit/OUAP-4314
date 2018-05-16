FROM python:3

RUN mkdir /home/soup/
WORKDIR /home/soup/

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "AddDatabase.py"]
