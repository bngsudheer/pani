.. Pani documentation master file, created by
   sphinx-quickstart on Sat Jul 12 19:41:01 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================
Welcome to Pani's documentation!
================================

.. toctree::
   :maxdepth: 2

Pani is a glue tool to put together various Mercurial extensions. The web application allows an administrator to manage projects and users.

=====================
Installation
=====================

* Install the required packages::

    # yum install python-virtualenv

* Create the user - mercurial::    

    # adduser mercurial

* Switch to mercurial user::

    # su - mercurial

* Create a Python virtual environment::

    $ virtualenv panienv


* Download the tarball::

    $ wget 'https://bitbucket.org/bngsudheer/paniweb/downloads/pani.tar.gz'

* Extract the tarball::

    $ tar -zxvf pani.tar.gz 

* Change directory::

    $ cd pani

* Install the Paniweb application::

    $ ~/panienv/bin/python setup.py install

* Paniweb requires a configuration file. The location of the configuration file should be set in your environment. For example, add this in your ~/.bashrc file::

    export PANI_SITE_SETTINGS=/home/mercurial/etc/pani.cfg

* The next time you login to the shell, the environment variable will be available. To make it available immediately::

    source ~/.bashrc 

* Create the directory for configuration::

    $ mkdir ~/etc

* Setup the database::

    $ cat pani/doc/schema.sql | sqlite3 pani.db

* Add the following to your configuration file(/home/mercurial/etc/pani.cfg)::

    SQLALCHEMY_DATABASE_URI='sqlite:////home/mercurial/pani/pani.db'
    SQLALCHEMY_ECHO='false'
    SESSION_SECRET_KEY='yetanothersecret'
    DEBUG=False
    AUTHORIZED_KEYS_PATH='/home/mercurial/.ssh/authorized_keys'
    BASE_PATH='/home/mercurial'

* Create .ssh directory if it does not exist alredy::

    ssh-keygen

The lazy way of creating the .ssh directory with appropriate permission.

* Run the application::

    $ ~/panienv/bin/python runserver.py

The application will be running on port 5006. Setup a proxt to put Pani behind a web server like Apache or Nginx if you wish. 

The default account details::

    username: admin
    password: password

To change the password, click Users and then click Edit button next to the user.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

