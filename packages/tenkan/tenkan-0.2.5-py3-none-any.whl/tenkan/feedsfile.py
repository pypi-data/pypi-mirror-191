#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" feedsfile mddule : json feeds file manipulation """

import json
import logging
from typing import Dict  # , Optional

from prettytable import PrettyTable


def create(file: str) -> None:
    """file creation"""
    with open(file, 'x') as _file:
        data: dict = {'feeds': {}}
        json.dump(data, _file)


def read(file: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """read file and return json data"""
    with open(file, 'r') as _file:
        file_data = json.load(_file)
    return file_data


def _write(file: str, file_data: Dict[str, Dict[str, Dict[str, str]]]) -> None:
    """write new data into file"""
    with open(file, 'w') as file_updated:
        json.dump(file_data, file_updated, indent=4)


def add_feed(file: str, feed_name: str, feed_url: str) -> None:
    """add a new feed into existing file"""
    file_data: Dict[str, Dict[str, Dict[str, str]]] = read(file)
    file_data['feeds'][feed_name] = {
        'url': feed_url,
        'last_update': '',
        'hash_last_update': '',
    }
    _write(file, file_data)
    logging.info('feed %s added', feed_name)


def del_feed(file: str, feed_name: str) -> None:
    """remove feed from file"""
    file_data = read(file)
    # don't do anything if no feed found
    if file_data['feeds'].get(feed_name):
        del file_data['feeds'][feed_name]
        _write(file, file_data)
        logging.info('feed %s deleted', feed_name)
    else:
        logging.info('no feed %s found into feeds file', feed_name)


def get_feed_item(file: str, feed_name: str, item: str) -> str:
    """Return element of a defined feed"""
    file_data = read(file)
    item = file_data['feeds'][feed_name][item]
    return item


def update_last_run(file: str, date: str) -> None:
    """Update last_run key in json file"""
    file_data: dict = read(file)
    file_data['last_run'] = date
    _write(file, file_data)


def update_feed(file: str, feed_name: str, hash_last_update: str) -> None:
    """update last update date of a defined feed"""
    file_data = read(file)
    file_data['feeds'][feed_name]['hash_last_update'] = hash_last_update
    _write(file, file_data)


def list_feeds(file: str) -> None:
    """list feed file content"""
    file_data = read(file)
    table = PrettyTable()
    table.field_names = ['Title', 'URL']
    for item, value in file_data['feeds'].items():
        table.add_row([item, value['url']])
    logging.info(table)
