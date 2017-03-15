# archon

Cisco Application Centric Manager

## 1. Install

### 1.1. Manual Install

#### 1.1.1. Install Mariadb

**Windows**
	
[MariaDB Link](https://downloads.mariadb.org/interstitial/mariadb-10.1.14/winx64-packages/mariadb-10.1.14-winx64.msi/from/http%3A//ftp.utexas.edu/mariadb/)

**Redhat/CentOS (tested on CentOS 7.x):**
	
	$ yum install epel-release
	$ yum install git gcc python-pip mariadb-server mariadb-devel python-devel
	$ systemctl enable mariadb
	$ systemctl start mariadb

**Ubuntu/Debian (tested on Ubuntu 14.04):** 

	$ apt-get install git gcc python-pip mariadb-server libmysqlclient-dev python-dev

#### 1.1.2. Install Python Package 

	$ pip install pygics django mysqlclient openpyxl

#### 1.1.3. Install Product Rest API Wrapper

[Acidipy Link](https://github.com/HyechurnJang/acidipy)

[Asadipy Link](https://github.com/HyechurnJang/asadipy)

#### 1.1.4. Create Database

Setting Variables
* {ADMIN_NAME} : ID for Administrator
* {PASSWORD} : Password for Administrator

First Run

	$ mysql_secure_installation

Connect mariadb server with client

	$ mysql -u root -p

Create database & auth

	mysql > CREATE DATABASE archon;
	mysql > GRANT ALL PRIVILEGES ON archon.* TO '{ADMIN_NAME}'@'localhost' IDENTIFIED BY '{PASSWORD}';"
	
{ADMIN_NAME} and {PASSWORD} is used for initial login ID & Password

#### 1.1.5. Initial Setting

Using Environments
* {ARCHON_ROOT} : Archon Package Root

Edit {ARCHON_ROOT}/application/__init__.py

	WSGI_DEBUG = True # if False then production level
	WSGI_HOSTS = [] # if WSGI_DEBUG is False then need to insert service IP
	LANGUAGE = '{DEFAULT_LANGUAGE}' # en or ko
	DATABASE_USER = '{ADMIN_NAME}'
	DATABASE_PASSWORD = '{PASSWORD}'

Important! {ADMIN_NAME} & {PASSWORD} is same as Variables in Create Database Section

#### 1.1.6. Setting Applications

Edit {ARCHON_ROOT}/application/{APPLICATION_NAME}/settings.py

	#===============================================================================
	# Archon Settings
	#===============================================================================
	ACTIVE = True # True = Enable Service, False = Disable Service
	DISPLAY = u'{APPLICATION_DISPLAYED_NAME}'
	
	#===============================================================================
	# Application Settings
	#===============================================================================
	...

#### 1.1.7. Django Initialization

	$ cd {ARCHON_ROOT}
	$ python manage.py makemigrations
	$ python manage.py migrate
	$ python manage.py createsuperuser

If ACI Application Enabled : Faults Data for ACI Application

	$ python manage.py loaddata apic_faults

* makemigrations : create python wrapper for database
* migrate : create database tables
* createsuperuser : create superuser
* loaddata : load fixture to database

#### 1.1.8 Running Server

	$ python server.py
