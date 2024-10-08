FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install dnspython

RUN pip3 install psycopg2-binary

COPY . .

CMD ["python3", "main.py"]