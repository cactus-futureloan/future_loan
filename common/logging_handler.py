import logging


def logging_handler(
        logger_name="root",
        logger_level="DEBUG",
        stream_level="DEBUG",
        fmt="%(asctime)s-[%(filename)s-->line:%(lineno)d--%(levelname)s:%(message)s]",
        file=None,
        file_level="INFO"
):
    """写日志"""
    # 获取收集器
    logger = logging.getLogger(logger_name)
    # 设置收集器等级
    logger.setLevel(logger_level)
    # 获取console输出处理器
    stream_handler = logging.StreamHandler()
    # 设置console输出处理器的等级
    stream_handler.setLevel(stream_level)
    # 定义日志格式
    log_fmt = logging.Formatter(fmt)
    # 设置console输出处理器的格式
    stream_handler.setFormatter(log_fmt)
    # 将console输出处理器添加到收集器
    logger.addHandler(stream_handler)
    # logger.removeHandler(stream_handler)

    if file:
        # 定义file输出处理器
        file_handler = logging.FileHandler(file, encoding="utf-8")
        # 设置file输出处理器的等级
        file_handler.setLevel(file_level)
        # 设置file输出处理器的格式
        file_handler.setFormatter(log_fmt)
        # 将file输出处理器添加到收集器
        logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    logger = logging_handler(logger_name="test1", file="log.txt")
    logger.info('这是info等级的日志')
