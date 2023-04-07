FROM python:3.10

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
WORKDIR /code/application

CMD flask run -h 0.0.0.0 -p 80