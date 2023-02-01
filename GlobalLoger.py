import logging
import logging.config
import os
import config


def get_logger(name='root'):
    conf_log = os.path.abspath(os.getcwd() + "/logger_config.ini")
    logging.config.fileConfig(conf_log)
    return logging.getLogger(name)

ta_log = get_logger(__name__)
