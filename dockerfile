FROM python:3.8

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN alembic upgrade head

CMD [ "python", "app.py" ]