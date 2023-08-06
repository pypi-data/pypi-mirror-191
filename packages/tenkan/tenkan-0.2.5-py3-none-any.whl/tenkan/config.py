# -*- coding: utf-8 -*-

"""config module : configuration file parsing"""

import configparser
import logging
import sys
from pathlib import Path


def load_config(config_file) -> configparser.ConfigParser:
    """config load"""

    # exit with error if config file not found
    if not Path(config_file).exists():
        logging.error('No config file found %s, exiting', config_file)
        sys.exit(1)

    parser = configparser.ConfigParser()
    parser.read(config_file)
    if 'tenkan' not in parser.sections():
        logging.critical(
            "Missing [tenkan] section in config file %s, can't go further",
            config_file,
        )
        sys.exit(1)

    # shitty checks of config content
    # to improve later...
    for opt in ['gemini_path', 'gemini_url']:
        if not parser.has_option('tenkan', opt):
            logging.error('Missing option %s', opt)
            sys.exit(1)

    if parser.has_option('tenkan', 'purge_feed_folder_after'):
        if not int(parser['tenkan']['purge_feed_folder_after']):
            logging.error(
                'Wrong type for purge_feed_folder_after option, should be a number'
            )
            sys.exit(1)

    if parser.has_section('filters'):
        for item in parser['filters']:
            parser['filters'][item] = parser['filters'][item].replace(' ', '')

    if parser.has_option('formatting', 'truncated_feeds'):
        parser['formatting']['truncated_feeds'] = parser['formatting'][
            'truncated_feeds'
        ].replace(' ', '')

    if parser.has_option('formatting', 'title_size') and not int(
        parser['formatting']['title_size']
    ):
        logging.error('Wrong type for title_size option, should be a number')
        sys.exit(1)

    return parser
