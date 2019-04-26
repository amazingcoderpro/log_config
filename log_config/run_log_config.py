#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/6/20
# Function: A simple example for using init_log_config()

from log_config import init_log_config
import logging
logger = logging.getLogger(__name__)


def produce_log():
    init_log_config(file_prefix="project_name")
    logger.debug("this is a message of debug level.")
    logger.info("this is a message of info level.")
    logger.warning("this is a message of info level.")
    logger.error("this is a message of error level.")


produce_log()
