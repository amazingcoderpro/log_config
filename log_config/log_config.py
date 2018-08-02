#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/6/20
# Function:
'''
Provide a function  for anyone who want to configure log parameters easily,
just call init_log_config before your use the module of logging that build-in python3
'''


import os
import logging
from datetime import datetime
from logging import handlers

# formatter
FORMATTER = "%(asctime)s %(filename)s[line:%(lineno)d] " \
            "[%(module)s:%(funcName)s] [%(threadName)s:%(thread)d] " \
            "%(levelname)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# log file args
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_NAME = "debug_{}.log".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))       # your_log_file_name.log
LOG_FILE_PATH = os.path.join(BASE_DIR, LOG_FILE_NAME)   # your log full path
LOG_FILE_SIZE = 10 * 1024 * 1024                        # the limit of log file size
LOG_BACKUP_COUNT = 5                                    # backup counts

# log mail args, You need to correct the following variables if you want to use email notification function
MAIL_SERVER = 'smtp.xxxx.com'
MAIL_PORT = 25
FROM_ADDR = 'from@xxx.com'
TO_ADDRS = "to1@xxx.com;to2@xxx.com"
SUBJECT = 'Application Error'
CREDENTIALS = ('your_account@xxx.com', 'your_password')

# log level args
LOG_OUTPUT_LEVEL = logging.DEBUG
LOG_FILE_LEVEL = logging.INFO
LOG_CONSOLE_LEVEL = logging.DEBUG
LOG_MAIL_LEVEL = logging.ERROR


def init_log_config(base_dir="", file_name_prefix="debug", file_size_limit=10*1024*1024, backup_count=10, use_mail=False):
    '''
    Do basic configuration for the logging system. support ConsoleHandler, RotatingFileHandler and SMTPHandler
    :param base_dir: the dir
    :param file_name_prefix: log file name prefix, default "debug"
    :param file_size_limit: log file size limit, default 10M
    :param backup_count: log file count, default 10
    :param use_mail: Whether to use the email notification function, default False
    :return: None
    '''

    try:
        logging.basicConfig(level=LOG_OUTPUT_LEVEL,
                            format=FORMATTER,
                            datefmt=DATE_FORMAT)

        # log file directory
        if not base_dir:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(base_dir, "{}_{}.log".format(file_name_prefix, datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

        # add rotating file handler
        rf_handler = handlers.RotatingFileHandler(log_file_path, maxBytes=file_size_limit, backupCount=backup_count)
        rf_handler.setLevel(LOG_FILE_LEVEL)
        formatter = logging.Formatter(FORMATTER)
        rf_handler.setFormatter(formatter)
        logging.getLogger().addHandler(rf_handler)

        # add smtp handler if use_mail is True
        if use_mail:
            mail_handler = handlers.SMTPHandler(
                mailhost=(MAIL_SERVER, MAIL_PORT),
                fromaddr=FROM_ADDR,
                toaddrs=TO_ADDRS.split(";"),
                subject=SUBJECT,
                credentials=CREDENTIALS
            )
            mail_handler.setLevel(LOG_MAIL_LEVEL)
            mail_handler.setFormatter(logging.Formatter(FORMATTER))
            logging.getLogger().addHandler(mail_handler)
    except Exception as e:
        print("init log config catch exception:{}".format(e))
        return False

    return True
