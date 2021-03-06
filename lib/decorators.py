import time
from datetime import datetime, timedelta
from functools import wraps

from loguru import logger


def log_exceptions(func):
    @wraps(func)
    def decorate(*a, **k):
        # noinspection PyBroadException
        try:
            func(*a, **k)
        except Exception as e:
            logger.exception(e)
            pass

    return decorate


def reset_midi_client(func):
    @wraps(func)
    def decorate(*a, **k):
        from api.client.p0_script_api_client import p0_script_client

        p0_script_client.IS_LIVE = False
        func(*a, **k)

    return decorate


class throttle(object):
    """
    Decorator that prevents a function from being called more than once every
    time period.
    """

    def __init__(self, milliseconds=0):
        self.throttle_period = timedelta(milliseconds=milliseconds)
        self.time_of_last_call = datetime.min

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*a, **k):
            time_since_last_call = datetime.now() - self.time_of_last_call

            if time_since_last_call <= self.throttle_period:
                logger.info(f"{fn} throttled. time_since_last_call: {time_since_last_call}")
                return

            res = fn(*a, **k)
            self.time_of_last_call = datetime.now()
            return res

        return wrapper


def timing(f):
    @wraps(f)
    def wrap(*a, **k):
        start_at = time.time()
        res = f(*a, **k)
        end_at = time.time()
        logger.info(f"func: {f.__name__} took: {end_at - start_at:.3f} sec")
        return res

    return wrap
