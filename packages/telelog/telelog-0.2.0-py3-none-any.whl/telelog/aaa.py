# For scripts
import os
import sys
from loguru import logger

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


if __name__ == "__main__":
    # logger.remove(0)
    # print(logger.level('DEBUG'))
    # print(logger.level('INFO'))
    # print(logger.level('WARNING'))
    # print(logger.level('ERROR'))
    # logger.level('WARN', no=30, color='<yellow><bold>', icon='⚠️')
    # logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file.path}:{line} \t{message}")
    # logger.info('Hello')
    # logger.warning('World')
    # logger.log('WARN', 'chatgpt')
    init_loguru(scene='digital')
    stdlog = logger.bind(name="stdlog")
    buslog = logger.bind(name="buslog")
    stdlog.debug("stdlog debug")
    stdlog.info("stdlog info")
    stdlog.log("WARN", "stdlog warning")
    stdlog.error("stdlog error")
    buslog.debug("buslog debug")
    buslog.info("buslog info")
    buslog.log("WARN", "buslog warning")
    buslog.error("buslog error")