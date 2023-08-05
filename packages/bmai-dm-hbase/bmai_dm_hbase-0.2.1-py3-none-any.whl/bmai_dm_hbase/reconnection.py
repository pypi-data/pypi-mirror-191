# -*- coding: utf-8 -*-


from thriftpy2.transport import TTransportException

from happybase import NoConnectionsAvailable


def reconnection(func,time=3):
    """
    处理多种连接异常:1.创建连接池异常  2.连接池取出异常
    """  
    def wrapper(*args, **kwargs):
        for i in range(time):
            try:
                return func(*args, **kwargs)
            except (TTransportException, TimeoutError):
                # if i >= 1:
                #     logger.warn(f"retry {i} times")
                pass
            except NoConnectionsAvailable:
                pass
            except Exception as e:
                raise e
        # logger.error(f"fail after retring {time} times")
        return []
    return wrapper