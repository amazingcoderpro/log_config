#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/6/20
# Function:
'''
Provide a function  for anyone who want to configure log parameters easily,
just call init_log_config before your use the module of logging that build-in python3
- support MultiProcessTimedRotatingFileHandler 支持多进程日志打印
'''


import os
import sys
import time
import fcntl
import logging
from datetime import datetime
# from logging import handlers
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler, SMTPHandler

# formatter
FORMATTER = "%(asctime)s [%(threadName)s] [%(filename)s:%(funcName)s:%(lineno)d] " \
            "%(levelname)s %(message)s"
DATE_FORMAT = "%Y%m%d_%H%M%S"

# log file args
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_NAME = "debug_{}.log".format(datetime.now().strftime("%Y%m%d_%H%M%S"))       # your_log_file_name.log
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
LOG_CONSOLE_LEVEL = logging.DEBUG
LOG_FILE_LEVEL = logging.INFO
LOG_MAIL_LEVEL = logging.ERROR


class MultiProcessTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    加锁保证删除文件的进程安全，支持多进程模式下日志打印，并按照时间分隔日志文件
    """
    _stream_lock = None

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + '.' + time.strftime(self.suffix, timeTuple)

        # 加锁保证rename的进程安全
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            fcntl.lockf(self.stream_lock, fcntl.LOCK_EX)
            try:
                if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                    os.rename(self.baseFilename, dfn)
            finally:
                fcntl.lockf(self.stream_lock, fcntl.LOCK_UN)

        # 加锁保证删除文件的进程安全
        if self.backupCount > 0:
            if self.getFilesToDelete():
                fcntl.lockf(self.stream_lock, fcntl.LOCK_EX)
                try:
                    files_to_delete = self.getFilesToDelete()
                    if files_to_delete:
                        for s in files_to_delete:
                            os.remove(s)
                finally:
                    fcntl.lockf(self.stream_lock, fcntl.LOCK_UN)

        if not self.delay:
            # _open默认是以‘a'的方式打开，是进程安全的
            self.stream = self._open()
            # 注释掉下面一行，解决写日志时偶现的 BrokenPipeError 错误
            # self.stream = FileObjectPosix(self.stream, 'wUb')   # 'U': use universal newlines

        newRolloverAt = self.computeRollover(currentTime)
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def computeRollover(self, currentTime, adjust_on_hour=True):
        """
        Compute the rollover time adjust on hour. 默认在每个整点重新生成新的日志文件
        :param currentTime:
        :param a djust_on_hour:
        :return:
        """
        newRolloverAt = super().computeRollover(currentTime)
        if adjust_on_hour and self.when.upper() == 'H':
            dt = datetime.fromtimestamp(newRolloverAt)
            current_hour = dt.replace(minute=0, second=0, microsecond=0)
            newRolloverAt = current_hour.timestamp()
            while newRolloverAt <= currentTime:
                newRolloverAt = newRolloverAt + self.interval
        return newRolloverAt

    @property
    def stream_lock(self):
        if not self._stream_lock:
            self._stream_lock = self._openLockFile()
        return self._stream_lock

    def _getLockFile(self):
        # Use 'file.lock' and not 'file.log.lock' (Only handles the normal "*.log" case.)
        if self.baseFilename.endswith('.log'):
            lock_file = self.baseFilename[:-4]
        else:
            lock_file = self.baseFilename
        lock_file += '.lock'
        return lock_file

    def _openLockFile(self):
        lock_file = self._getLockFile()
        return open(lock_file, 'a')



def init_log_config(log_dir="", file_prefix="debug", file_size_limit=20 * 1024 * 1024, backup_count=30,
                    use_mail=False, console_level=LOG_CONSOLE_LEVEL,
                    file_level=LOG_FILE_LEVEL, mail_level=LOG_MAIL_LEVEL, when="midnight", interval=1,
                    crated_time_in_file_name=False, multi_process=False):
    '''
    Do basic configuration for the logging system. support ConsoleHandler, RotatingFileHandler and SMTPHandler
    :param log_dir: the dir where to save log files, default "{current_path}/logs"
    :param file_prefix: log file name prefix, default "debug"
    :param file_size_limit: log file size limit, default 10M
    :param backup_count: log file count, default 10
    :param use_mail: Whether to use the email notification function, default False
    :param console_level: the level of output log in console, default logging.DEBUG
    :param file_level: the level of log file, default logging.INFO
    :param mail_level: the level of log mail, default logging.ERROR
    :param when: rotating the log file at certain timed intervals. 'D'-days, 'H'-hours, 'M'-minutes
    :param interval: rotating the log file at certain timed intervals.
    :param crated_time_in_file_name: Whether to create a log file with a time stamp in the file name, default False
    :param multi_process: Whether support multi-process situation to rotate log file, default False
    :return: None
    '''

    try:
        logging.basicConfig(level=console_level,
                            format=FORMATTER,
                            datefmt=DATE_FORMAT)

        # log file directory
        if not log_dir:
            log_dir = os.path.join(sys.path[0], "logs")
            # log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)

        # default log file name like: debug_2018-08-27_15-40-52.log
        if crated_time_in_file_name:
            log_file_path = os.path.join(log_dir, "{}_{}.log".format(file_prefix, datetime.now().strftime("%Y%m%d_%H%M%S")))
        else:
            log_file_path = os.path.join(log_dir, "{}.log".format(file_prefix))

        # add rotating file handler
        # rf_handler = handlers.RotatingFileHandler(log_file_path, maxBytes=file_size_limit, backupCount=backup_count, encoding="utf-8")
        if when:
            if multi_process:
                rf_handler = MultiProcessTimedRotatingFileHandler(log_file_path, when=when, backupCount=backup_count, interval=interval, encoding="utf-8")
            else:
                rf_handler = TimedRotatingFileHandler(log_file_path, when=when, backupCount=backup_count, interval=interval, encoding="utf-8")
        else:
            rf_handler = RotatingFileHandler(log_file_path, maxBytes=file_size_limit, backupCount=backup_count, encoding="utf-8")

        rf_handler.setLevel(file_level)
        formatter = logging.Formatter(FORMATTER)
        rf_handler.setFormatter(formatter)
        logging.getLogger().addHandler(rf_handler)

        # add smtp handler if use_mail is True
        if use_mail:
            mail_handler = SMTPHandler(
                mailhost=(MAIL_SERVER, MAIL_PORT),
                fromaddr=FROM_ADDR,
                toaddrs=TO_ADDRS.split(";"),
                subject=SUBJECT,
                credentials=CREDENTIALS
            )
            mail_handler.setLevel(mail_level)
            mail_handler.setFormatter(logging.Formatter(FORMATTER))
            logging.getLogger().addHandler(mail_handler)
    except Exception as e:
        print("init log config catch exception:{}".format(e))
        return False

    return True
