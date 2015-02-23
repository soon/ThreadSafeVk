import logging
import sys

__author__ = 'Andrew Kuchev (kuchevad@gmail.com)'

__all__ = ['safe_call', 'log_if_failed', 'safe_call_and_log_if_failed']


def safe_call(unsafe_function):
    """
    Decorator for making function safe

    :return: Function, which returns tuple of two elements:
             - (True, result)     - no error, result is returned
             - (False, exception) - error has occurred
    """
    def wrapper(*args, **kwargs):
        try:
            return True, unsafe_function(*args, **kwargs)
        except Exception, e:
            e.exc_info = sys.exc_info()
            return False, e

    return wrapper


def log_if_failed(function=None, default=None):
    """
    Decorator for logging safe function if error has occurred
    :param default: Returned, if error has occurred
    :return: Function, which returns result if no error,
                                else default
    """
    def log_if_failed_with_default(safe_function):
        def wrapper(*args, **kwargs):
            succeed, result_or_error = safe_function(*args, **kwargs)
            result = default if not succeed else result_or_error
            if not succeed:
                logging.error(result_or_error, exc_info=result_or_error.exc_info)
            return result

        return wrapper

    if function is not None:
        return log_if_failed_with_default(function)
    return log_if_failed_with_default


def safe_call_and_log_if_failed(function=None, default=None):
    """
    Just combination of safe_call and log_if_failed
    :param default:
    :return:
    """
    def wrapper(unsafe_function):
        return log_if_failed(safe_call(unsafe_function), default)

    if function is not None:
        return wrapper(function)
    return wrapper