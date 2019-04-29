====================
Log_Config
====================

Provide a function for anyone who want to configure log parameters easily, just call init_log_config when your app start up, the you can use the module of logging which build-in python3 without any other configtur. This module support ConsoleHandler, RotatingFileHandler and SMTPHandler and You can change the configuration parameters according to your requirements.


Meta
----

* Author: Wu Charles
* Email:  wcadaydayup@163.com
* Maintainer: Wu Charles
* Email: wcadaydayup@163.com
* Status: active development, stable, maintained

[![Version](https://img.shields.io/pypi/v/log_config.svg)](https://pypi.python.org/pypi/log_config)
[![GitHub](https://github.com/wcadaydayup/log_config.svg?branch=master)](https://github.com/wcadaydayup/log_config)


Installation
------------
Simply run the following from within a virtualenv::

	$ pip install log_config
	
	or

        $ pip install git+https://github.com/wcadaydayup/log_config


Usage
-----
Import the log config function in anywhere you want use logging which build-in Python3::

    from log_config.log_config import init_log_config

Call init_log_config() when your application start up, of course you can modify log file path, log level and so on by import other variable from log_config.log_config::

    init_log_config()

Log confiture is ready, you can use logging module without any other configture::

    import logging
	logger = logging.getLogger()
	logger.debug("this is a message of debug level.")

Then, you will see you output message in console and log file which in your current directory::

    configure_installed_apps_logger(logging.INFO, verbose=True, filename='django-project.log')

You can also receive email notify if call init_log_config(use_mail=True), of course you should provide correct email parameters::

	import log_config.log_config as lf
	lf.EMAIL_HOST = "xxx.smtp.com"
	lf.FROM = "youraccount@xx.com"
	lf.TO = "a@xx.com;b@xx.com"
	
	...
	
    init_log_config(use_mail=True)


