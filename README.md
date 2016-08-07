# gtools-python
A re-write of gurrilla tools in Python with the Django framework.

Built with: Django==1.10, MySQL-python==1.2.5, django-bootstrap3==7.0.1

## Install

To get a basic copy running with the built in httpd, there should just be a few steps from a clean system:

Virtualenv is a good idea, but I leave that up to you. You'll want to have python, django, and the database libraries of your choice. (MySQL by default in this project.)

* Example for Debian/Ubuntu: `apt-get install python-pip python-dev libmysqlclient-dev`
* Install Python libraries: `pip install -r requirements.txt`
* Check out the code: `git clone https://github.com/lkmhaqer/gtools-python.git`
* Move to your new directory: `cd gtools-python`

Once you have your database, and user setup for mysql, simply run django's migrate command. Alternatively, set the backend to sqlite3 in gtools/settings.py and specifiy a file instead of using mysql, then migrate.

* Django's migrate command: `python manage.py migrate`
* Create an admin user: `python manage.py createsuperuser`
* Start the webserver on all IPs: `python manage.py runserver 0.0.0.0:8000`

Now you should be able to navigate to your host on port 8000 and see your new gtools install!
