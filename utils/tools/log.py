import logging
import logging.config
import logging.handlers

from .configManager import BASE_DIR, ConfigReader

__all__ = ['info_logger', 'error_logger']


LogConfig = dict(  # no cov
    version=1,
    loggers={
        "info_logger": {
            "level": "INFO",
            "handlers": ["info_file"],
            "propagate": True,
        },
        "error_logger": {
            "level": "INFO",
            "handlers": ["error_file"],
        },
    },
    handlers={
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(BASE_DIR) + ConfigReader().get_config('LogSetting', 'log_dir') + "/error.log",
            "when": ConfigReader().get_config('LogSetting', 'rotate_time'),
            "backupCount": int(ConfigReader().get_config('LogSetting', 'backup_count')),
            "encoding": "utf-8"
        },
        "info_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(BASE_DIR) + ConfigReader().get_config('LogSetting', 'log_dir') + '/info.log',
            "when": ConfigReader().get_config('LogSetting', 'rotate_time'),
            "backupCount": int(ConfigReader().get_config('LogSetting', 'backup_count')),
            "encoding": "utf-8"
        },
    },
)

logging.config.dictConfig(LogConfig)

info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')
