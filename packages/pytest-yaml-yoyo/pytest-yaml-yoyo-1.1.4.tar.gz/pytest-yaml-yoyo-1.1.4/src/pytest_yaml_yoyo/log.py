import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)


def set_log_format(config):
    """设置 log 日志格式"""
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    # log_file default log file name
    if not config.getini('log_file') and not config.getoption('log_file'):
        config.option.log_file = Path(config.rootdir).joinpath('logs', f'{current_time}.log')
    if not config.getini('log_file_level') and not config.getoption('log_file_level'):
        config.option.log_file_level = "info"
    if config.getini('log_file_format') == '%(levelname)-8s %(name)s:%(filename)s:%(lineno)d %(message)s' \
            and not config.getoption('log_file_format'):
        config.option.log_file_format = "%(asctime)s [%(levelname)s]: %(message)s"
    if config.getini('log_file_date_format') == '%H:%M:%S' and not config.getoption('log_file_date_format'):
        config.option.log_file_date_format = "%Y-%m-%d %H:%M:%S"
    # 设置 日志文件在控制台的输出格式
    if not config.getini('log_cli_format') and not config.getoption('log_cli_format'):
        config.option.log_cli_format = '%(asctime)s [%(levelname)s]: %(message)s'
    if not config.getini('log_cli_date_format') and not config.getoption('log_cli_date_format'):
        config.option.log_cli_date_format = '%Y-%m-%d %H:%M:%S'
