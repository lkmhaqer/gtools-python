# file: docker/Dockerfile

FROM python:2.7-alpine3.7

# Copy our requirements over first.
COPY requirements.txt /requirements.txt

# Add all the packages needed.
RUN set -ex \
    && apk add --no-cache \
            gcc \
            make \
            nginx \
            musl-dev \
            libc-dev \
            linux-headers \
            mariadb-dev \
    && pip install -U pip \
    && pip install uwsgi supervisor \
    && pip install -r /requirements.txt 

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

# Copy nginx configuration over.
COPY docker/nginx-app.conf /etc/nginx/nginx.conf

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL=none python manage.py collectstatic --noinput

# nginx will listen on this port
EXPOSE 80

# Start supervisor
CMD ["supervisord", "--nodaemon", "--configuration", "/code/docker/supervisor-app.conf"]
