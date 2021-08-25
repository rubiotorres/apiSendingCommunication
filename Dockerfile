FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app

RUN python manage.py makemigrations
RUN python manage.py makemigrations app
RUN python manage.py migrate