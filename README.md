# gtools-python 0.0.8

A configuration generation tool for networking devices. Written in python with Django as web framework and ORM. Define network information like ports, addressing, and routing neighborships, then generate network device configurations based on templates. Examples for IOS, JunOS, BIRD and Quagga included.

Built with:

Django==1.11.13
django-bootstrap3==10.0.1
Jinja2==2.9.5
MarkupSafe==0.23
MySQL-python==1.2.5
pytz==2018.4

## Docker Install

Public docker images now available: https://hub.docker.com/r/slothlogistics/gtools/

You only need one variable to start gtools:

```
host$ docker run slothlogistics/gtools \
      --name gtools -d \
      -e GTOOLS_SECRET_KEY="really-long-secret-key-here"
```

You can set all the database variables as well, the defaults are the values below.

```
host$ docker run slothlogistics/gtools \
      --name gtools -d \
      -e GTOOLS_SECRET_KEY="really-long-secret-key-here" \
      -e GTOOLS_DB_HOST="mysql" \
      -e GTOOLS_DB_NAME="gtools" \
      -e GTOOLS_DB_USER="gtools" \
      -e GTOOLS_DB_PASS="gtools_password"
```

After that, you should be up and running! Please report any issues. If you don't already have a mysql installation or container running, you can use the two steps below to get going super quick.

```
host$ docker run mysql:5.7 \
      --name gtools-mysql -d \
      -e MYSQL_ROOT_PASSWORD=test \
      -e MYSQL_DATABASE=gtools \
      -e MYSQL_USER=gtools \
      -e MYSQL_PASSWORD="gtools-password"

...
host$ docker run slothlogistics/gtools -d \
      --name gtools --link gtools-mysql:mysql \
      -e GTOOLS_SECRET_KEY="really-long-secret-key-here" \
      -e GTOOLS_DB_PASS="gtools-password"
```

This will start two containers, one for gtools the app, and one for mysql. Docker compose may come in the future.

## Lab or Development Install

To get a basic copy running with the built in httpd, there should just be a few steps from a clean system:

Virtualenv is a good idea, but I leave that up to you. You'll want to have python, django, and the database libraries of your choice. (MySQL by default in this project.)

* Example for Debian/Ubuntu: `apt-get install python-pip python-dev libmysqlclient-dev`
* Install Python libraries: `pip install -r requirements.txt`
* Check out the code: `git clone https://github.com/lkmhaqer/gtools-python.git`
* Move to your new directory: `cd gtools-python`

Setup a database, and user with permissions to it, then update gtools/settings.py with these details. Now you're ready to run django's migrate command. Alternatively, set the backend to sqlite3 in gtools/settings.py (see example below "SQLite Settings") and specifiy a file instead of using mysql, then migrate.

* Django's migrate command: `python manage.py migrate`
* Create an admin user: `python manage.py createsuperuser`
* Start the webserver on all IPs: `python manage.py runserver 0.0.0.0:8000`

Now you should be able to navigate to your host on port 8000 and see your new gtools install!

## Device Specific Template Files

So, you have all your data in gtools, now to generate router configs! All device configs are located in `$INSTALL_DIR/config_gen/templates/config_gen/`, some examples are included for JunOS, BIRD, Quagga, IOS, and a YAML dictionary. Feel free to open an issue for a template on a new network platform. If you've created your own templates, and are able to share, feel free to submit them to me, or just a pull request.

## SQLite Settings

If you would like to get going quick, and don't want to use MySQL, there is SQLite. The data will be saved to a file db.sqlite3, in your $INSTALL_DIR. To use it, instead of mysql, just replace the DATABASE variable block in gtools/settings.py with the following:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR , 'db.sqlite3'),
    }
}
```
