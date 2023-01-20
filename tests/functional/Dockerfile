FROM python:3.9

WORKDIR /tests/functional

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["/tests/functional/docker-entrypoint.sh"]


# FROM python:3.9.7

# WORKDIR /usr/src/app

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# COPY . .