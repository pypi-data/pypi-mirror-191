# -*- coding: utf-8 -*-

"""utils module : various utils"""

import logging
from time import sleep, time


def display_feeds_fetch_progress(fetched_feeds: list) -> None:
    """Display feeds being fetched"""
    qsize = len(fetched_feeds)
    while True:
        done = len([x for x in fetched_feeds if x['fetched_content'].done()])
        print(f'Fetching feeds [{done}/{qsize}]', end='\r', flush=True)
        sleep(0.3)
        if done == qsize:
            break


def measure(func):
    """
    Decorator to measure time took by a func
    Used only in debug mode
    """

    def wrap_func(*args, **kwargs):
        time1 = time()
        result = func(*args, **kwargs)
        time2 = time()
        logging.debug(
            'Function %s executed in %ss', func.__name__, time2 - time1
        )
        return result

    return wrap_func
