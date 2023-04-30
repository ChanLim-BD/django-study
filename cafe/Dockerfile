FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /cafe
WORKDIR /cafe
COPY requirements.txt /cafe/
RUN pip install -r requirements.txt
COPY . /cafe/

RUN python manage.py migrate

CMD [ "python manage.py runserver 0.0.0.0:8000" ]

# docker build -t cafe-django .