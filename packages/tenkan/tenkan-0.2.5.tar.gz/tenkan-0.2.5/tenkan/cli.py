# -*- coding: utf-8 -*-

"""
cli module
It parses args and runs what's needed if every over modules
depending of what command is done
"""

import configparser
import logging
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from pathlib import Path
from typing import NoReturn

from rich.traceback import install

from tenkan.config import load_config
from tenkan.feedsfile import (
    add_feed,
    create,
    del_feed,
    list_feeds,
    update_last_run,
)
from tenkan.files import delete_folder
from tenkan.processing import (
    fetch_feeds,
    prepare_fetched_content,
    process_fetched_feeds,
    write_processed_feeds,
)

# rich tracebacks
install(show_locals=True)


class MyParser(ArgumentParser):  # pylint: disable=too-few-public-methods
    """Child class to print help msg if no or bad args given"""

    def error(self, message: str) -> NoReturn:
        """exit"""
        sys.stderr.write(f'error: {message}')
        self.print_help()
        sys.exit(2)


def load_args(args: list):
    """args parsing function"""

    desc = 'tenkan : RSS/atom feed converter from html to gemini\n\nTo show the detailed help of a COMMAND run `ytcc COMMAND --help`.'
    parser = MyParser(
        description=desc, prog='tenkan', formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.1.0',
        help='show %(prog)s version number and exit',
    )

    parser.add_argument(
        '--config',
        default=f'{str(Path.home())}/.config/tenkan/tenkan.conf',
        help='config file, $HOME/.config/tenkan/tenkan.conf by default',
        dest='config',
    )
    parser.add_argument(
        '--feedsfile',
        default=f'{str(Path.home())}/.config/tenkan/feeds.json',
        help='feeds file containing feed list, $HOME/.config/tenkan/feeds.json by default',
        dest='feedsfile',
    )

    parser.add_argument(
        '--debug', action='store_true', help='debug mode', dest='debug'
    )

    subparsers = parser.add_subparsers(
        title='command', required=True, dest='command'
    )

    parser_add = subparsers.add_parser(
        'add', help='add a feed to the feeds list'
    )
    parser_add.add_argument(
        'name', help='the name of the feed you want to add'
    )
    parser_add.add_argument('url', help='the HTTP url of the feed')

    parser_update = subparsers.add_parser(
        'update', help='update feeds folder from feed list'
    )
    parser_update.add_argument(
        '--force',
        action='store_true',
        default=False,
        help='update feed list even if there is no new content',
    )

    parser_list = subparsers.add_parser(
        'list', help='list all feeds in feeds list'
    )
    parser_list.add_argument(
        'list', help='list all feeds in feeds list', action='store_true'
    )

    parser_delete = subparsers.add_parser(
        'delete', help='remove a feed to the feeds list'
    )
    parser_delete.add_argument(
        'name', help='the name of the feed you want to delete'
    )
    parser_delete.add_argument(
        '--delete-gmi-folder',
        help='delete gmi folder, True by default',
        action='store_true',
        default=False,
        dest='delete_folder',
    )
    return parser.parse_args(args)


def set_logging(args, config: configparser.ConfigParser) -> None:
    """define logging settings"""
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    if args.debug:
        log.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter(fmt='%(message)s')
    file_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s'
    )

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(console_formatter)
    log.addHandler(stdout_handler)

    if config['tenkan'].get('log_file'):
        file_handler = logging.FileHandler(
            filename=config['tenkan'].get('log_file'),
            encoding='utf-8',
        )
        file_handler.setFormatter(file_formatter)
        log.addHandler(file_handler)


def run(args, config: configparser.ConfigParser) -> None:
    """run stuff depending of command used"""
    # exit with error if json file not found with actions other than add
    if not Path(args.feedsfile).exists() and 'add' not in args.command:
        logging.error('No json file %s, can\'t continue', args.feedsfile)
        sys.exit(1)

    # list feeds in a pretty format
    if args.command == 'list':
        list_feeds(file=args.feedsfile)

    # add a feed to feeds file
    if args.command == 'add':
        # if home directory, creates json with empty structure if no file yet
        if not Path(args.feedsfile).parents[0].exists():
            if str(Path(args.feedsfile).parents[0]) == str(Path.home()):
                Path(args.feedsfile).parents[0].mkdir(
                    parents=True, exist_ok=True
                )
            else:
                logging.error(
                    'Directory of feeds file %s not found, exiting',
                )
                sys.exit(1)
        if not Path(args.feedsfile).is_file():
            create(args.feedsfile)
        add_feed(file=args.feedsfile, feed_name=args.name, feed_url=args.url)

    # delete a feed from feeds file
    if args.command == 'delete':
        del_feed(file=args.feedsfile, feed_name=args.name)
        if args.delete_folder:
            delete_folder(
                path=config['tenkan']['gemini_path'], feed_name=args.name
            )

    # update content
    if args.command == 'update':
        fetched_feeds = fetch_feeds(
            feeds_file=args.feedsfile,
            gmi_url=config['tenkan']['gemini_url'],
        )
        print('')
        fetched_feeds = prepare_fetched_content(fetched_feeds, args.force)
        feed_list = process_fetched_feeds(
            config=config,
            fetched_feeds=fetched_feeds,
            force=args.force,
        )
        if feed_list:
            write_processed_feeds(args, config, feed_list)
        else:
            logging.info('No new content to process, stopping')
        update_last_run(args.feedsfile, str(datetime.now()))


def main() -> None:
    """load conf, args, set logging and run main program"""

    args = load_args(args=sys.argv[1:])
    config = load_config(args.config)
    set_logging(args, config)
    run(args, config)
