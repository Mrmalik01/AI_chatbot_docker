FROM python:3.6
FROM kennethreitz/pipenv as build
WORKDIR /usr/src/app
COPY Pipfile .
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install && pipenv lock -r > requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD python3 app.py
