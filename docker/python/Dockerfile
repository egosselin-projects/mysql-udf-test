FROM python:3

WORKDIR /usr/src/app

CMD tar -czh . | docker build -

COPY requirements.txt ./requirements.txt
COPY main.py ./main.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./main.py" ]