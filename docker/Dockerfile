# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \ 
    apt-get install -y \
	git \
        libmysqlclient-dev \
	python \
	python-dev \
	python-setuptools \
	python-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip install -U pip setuptools && \
  	rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY docker/nginx-app.conf /etc/nginx/sites-available/default
COPY docker/supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installinig (all your) dependencies when you made a change a line or two in your app.

COPY requirements.txt /home/docker/code/app/
RUN pip install -r /home/docker/code/app/requirements.txt

# add (the rest of) our code
COPY docker/uwsgi.ini /home/docker/code
COPY docker/uwsgi_params /home/docker/code
COPY . /home/docker/code/app/
RUN rm -rfv /home/docker/code/app/docker

EXPOSE 80
CMD ["supervisord", "-n"]
