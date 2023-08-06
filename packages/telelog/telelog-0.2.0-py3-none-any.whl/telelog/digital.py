import os
from loguru import logger


def init_loguru(
        config=None, scene='default', log_dir='', log_path='', 
        level='INFO', enqueue=True, serialize=False
    ):
    '''
    config: 配置文件, 如果不为None, 按照配置进行初始化
    scene: 典型场景, 可以设置为default, ibox, digital
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
            logger.level('DEBUG', no=10, color='<blue><bold>', icon='🐞')
            logger.level('INFO', no=20, color='<bold>', icon='ℹ️')
            logger.level('WARN', no=30, color='<yellow><bold>', icon='⚠️')
            logger.level('ERROR', no=40, color='<red><bold>', icon='❌')
            logger.add(
                level=level,
                sink=os.path.join(log_dir, 'stdout.log'),
                format='{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file.path}:{line} \t{message}',
                filter=lambda record: record['extra']['name'] == 'stdlog' and str(record['level']).upper != 'ERROR',
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
                filter=lambda record: str(record['level']).upper == 'ERROR',
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
                filter=lambda record: record['extra']['name'] == 'buslog' and str(record['level']).upper != 'ERROR',
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