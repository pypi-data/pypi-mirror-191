
import os
import sys
import time
import logging
from loguru import logger
from threading import Thread
from logging.handlers import TimedRotatingFileHandler

ALLOW_LOG_LEVEL = ['FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
DYNAMIC_THREAD = False


'''
log_path: 日志路径
backup_count: 日志备份数量
terminal: 是否终端显示 True/False
dynamic_level: 是否动态变化 True/False
dynamic_interval: 冬天变化间隔时间
log_format: 日志格式 default/digital_life
when_time: 日志切分间隔 midnight/S/M/H/D/W
'''
def get_logger(logger=None, name='tele', level='info', log_path=None, backup_count=7, terminal=True,
               dynamic_level=False, dynamic_interval=30, log_format='default', when_time = 'midnight'):
    # 默认仅提供级别：FATAL, ERROR, WARNING, INFO, DEBUG
    logging.addLevelName(logging.DEBUG, 'DEBUG')
    logging.addLevelName(logging.INFO, 'INFO ')
    logging.addLevelName(logging.WARNING, 'WARN ')
    logging.addLevelName(logging.ERROR, 'ERROR')
    logging.addLevelName(logging.FATAL, 'FATAL')

    if logger:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
        logger.propagate = True
    else:
        logger = logging.getLogger(name)
    
    if log_format == "digital_life": # 数字生活日志格式
        logging.Formatter.default_msec_format = '%s.%03d'
        logging.Formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
        log_formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(pathname)s:%(lineno)s\t%(message)s')
    else: # 默认日志格式
        logging.Formatter.default_msec_format = '%s.%03d'
        logging.Formatter.default_time_format = '%Y%m%dT%H:%M:%S'
        log_formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(lineno)s %(threadName)s - %(message)s')
        
    if log_path is not None:
        handler = TimedRotatingFileHandler(log_path, when=when_time, interval=1, backupCount=backup_count)
        handler.suffix = '%Y-%m-%d'
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)

    if terminal:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)
    log_level = level.upper().strip()
    if log_level not in ALLOW_LOG_LEVEL:
        logger.warning(f'Init: LOG_LEVEL {log_level} is not allowed, set to default INFO')
        log_level = "INFO"
    logger.setLevel(log_level)
    global DYNAMIC_THREAD
    if dynamic_level and not DYNAMIC_THREAD:
        DYNAMIC_THREAD = True
        dynamic_level_thread = Thread(target=dynamic_change_log_level, args=(logger, log_level, dynamic_interval),
                                      name='LogThread')
        dynamic_level_thread.setDaemon(True)
        dynamic_level_thread.start()

    return logger


def dynamic_change_log_level(logger, log_level, dynamic_interval):
    logger = logger
    current_log_level = log_level
    dynamic_interval = dynamic_interval
    logger.info('Init: Start dynamic log level thread succeed')
    while True:
        log_level = os.environ.get('LOG_LEVEL', None)
        if log_level is not None:
            log_level = log_level.upper().strip()
            if log_level in ALLOW_LOG_LEVEL and log_level != current_log_level:
                logger.setLevel(log_level)
                if log_level == 'ERROR':
                    logger.error(f'Timer: Change LOG_LEVEL from {current_log_level} to {log_level}')
                if log_level == 'WARNING':
                    logger.warning(f'Timer: Change LOG_LEVEL from {current_log_level} to {log_level}')
                else:
                    logger.info(f'Timer: Change LOG_LEVEL from {current_log_level} to {log_level}')
        time.sleep(dynamic_interval)



def init_loguru(
        scene='default', log_dir='./', log_path='./stdout.log', 
        level='INFO', enqueue=True, serialize=False, config=None
    ):
    '''
    scene: 典型场景, 可以设置为default, ibox, digital
    config: 配置文件, 如果不为None, 按照配置进行初始化
    '''
    logger.remove(0)
    if config is None:
        if scene == 'default':
            logger.add(
                sink='stdout.log',
                format='{level} {time:YYYYMMDD HH:mm:ss} {file}:{line} {thread.name} - {message}',
                filter=lambda x: x == True,
                backtrace=True,
                diagnose=True,
                rotation='00:00',
                compression='zip',
                retention='100 days',
                enqueue=enqueue
            )
        elif scene == 'ibox':
            logger.add(
                level=level,
                sink=log_path,
                format='{level} {time:YYYYMMDD HH:mm:ss} {file}:{line} {thread.name} - {message}',
                backtrace=True,
                diagnose=True,
                rotation='00:00',
                compression='zip',
                retention='10 days',
                enqueue=enqueue,
                serialize=serialize
            )
        elif scene == 'digital':
            logger.level('WARN', no=30, color='<yellow><bold>', icon='⚠️')
            logger.add(
                level=level,
                sink=os.path.join(log_dir, 'stdout.log'),
                format='{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file.path}:{line} \t{message}',
                filter=lambda record: record['extra']['name'] == 'stdlog' and 'ERROR' not in str(record['level']).upper(),
                backtrace=True,
                diagnose=True,
                rotation='00:00',
                compression='zip',
                retention='100 days',
                enqueue=enqueue,
                serialize=serialize
            )
            logger.add(
                level=level,
                sink=os.path.join(log_dir, 'stderr.log'),
                format='{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file.path}:{line} \t{message}',
                filter=lambda record: 'ERROR' in str(record['level']).upper(),
                backtrace=True,
                diagnose=True,
                rotation='00:00',
                compression='zip',
                retention='100 days',
                enqueue=enqueue,
                serialize=serialize
            )
            logger.add(
                level=level,
                sink=os.path.join(log_dir, 'business.log'),
                format='{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file.path}:{line} \t{message}',
                filter=lambda record: record['extra']['name'] == 'buslog' and 'ERROR' not in str(record['level']).upper(),
                backtrace=True,
                diagnose=True,
                rotation='00:00',
                compression='zip',
                retention='100 days',
                enqueue=enqueue,
                serialize=serialize    
            )
    else:
        logger.configure(**config)
