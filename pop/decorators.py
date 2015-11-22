__author__ = 'austin'

from threading import Thread


def async(f):
    """
        Uses simple threading to run task in the background.
        Good for large processing and background updates.
    :param f: function to run in the background
    :return: wrapped function
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

