FROM python:3

RUN mkdir /home/soup/
WORKDIR /home/soup/

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]
CMD ["AddDatabase.py"]
