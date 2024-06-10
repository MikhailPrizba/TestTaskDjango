FROM python:3.11.9

WORKDIR /project

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="."
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy
COPY . .
RUN chmod a+x entrypoint/*.sh