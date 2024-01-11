import logging
import sys
from component.ConfigManager import config_manager


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


class LogManager:
    """
    初始化日志管理器和格式化
    """

    def __init__(self):
        log_level = config_manager.get_value(['log_level'])

        self.root_logger = logging.getLogger()
        if log_level == 'info':
            self.root_logger.setLevel(logging.INFO)
        elif log_level == 'debug':
            self.root_logger.setLevel(logging.DEBUG)
        elif log_level is None:
            self.root_logger.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(filename)s: %(message)s')

        # stdout 日志
        handler_out = logging.StreamHandler(sys.stdout)
        handler_out.setLevel(logging.DEBUG)
        handler_out.setFormatter(formatter)
        handler_out.addFilter(InfoFilter())

        # stderr 日志
        handler_err = logging.StreamHandler(sys.stderr)
        handler_err.setFormatter(formatter)
        handler_err.setLevel(logging.WARNING)

        self.root_logger.addHandler(handler_out)
        self.root_logger.addHandler(handler_err)

        # 根据配置文件判断，是否要写入到文件
        try:
            if config_manager.get_value(['log', 'to_file']):
                # 写入到文件 (out)
                file_handler_out = logging.FileHandler(config_manager.get_value(['log', 'output']))
                file_handler_out.setLevel(logging.DEBUG)
                file_handler_out.setFormatter(formatter)

                # 写入到文件 (err)
                file_handler_err = logging.FileHandler(config_manager.get_value(['log', 'error']))
                file_handler_err.setLevel(logging.WARNING)
                file_handler_err.setFormatter(formatter)

                self.root_logger.addHandler(file_handler_out)
                self.root_logger.addHandler(file_handler_err)
        except Exception as e:
            pass

    def get_logger(self, name):
        return logging.getLogger(name)


log_manager: LogManager = LogManager()

__all__ = [log_manager]