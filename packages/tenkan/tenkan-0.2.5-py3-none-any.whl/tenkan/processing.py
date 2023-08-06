# -*- coding: utf-8 -*-

"""processing module : feeds file processing """

import configparser
import hashlib
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor

import feedparser  # type: ignore

from tenkan.feed import Feed
from tenkan.feedsfile import read, update_feed
from tenkan.files import path_exists, write_files
from tenkan.utils import display_feeds_fetch_progress, measure


@measure
def fetch_feeds(feeds_file: str, gmi_url: str) -> list:
    """Fetch all http feeds with threads"""
    workers = os.cpu_count() or 1
    try:
        fetched_feeds = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for item, values in read(feeds_file)['feeds'].items():
                fetched_feeds.append(
                    {
                        'title': item,
                        'fetched_content': executor.submit(
                            feedparser.parse, values['url']
                        ),
                        'gmi_url': gmi_url,
                        'last_update': values['last_update'],
                        'fetched_hash_last_update': None,
                        'json_hash_last_update': values['hash_last_update'],
                    }
                )
            display_feeds_fetch_progress(fetched_feeds)
        return fetched_feeds
    except json.decoder.JSONDecodeError as bad_json:
        raise bad_json


@measure
def prepare_fetched_content(fetched_feeds: list, force: bool = False) -> list:
    """Prepare some necessary data to be sent to feed object"""
    list_to_export = []
    for ftfd in fetched_feeds:
        try:
            # store workers result into fetched_content
            ftfd['fetched_content'] = ftfd['fetched_content'].result()  # type: ignore
            # we store a sha256 footprint of fetched content,
            # to compare to last known footprint
            tmp_hash = hashlib.sha256(
                str(ftfd['fetched_content'].get('entries')[0]).encode()
            )
            if tmp_hash.hexdigest() != ftfd['json_hash_last_update'] or force:
                ftfd['fetched_hash_last_update'] = tmp_hash.hexdigest()
                list_to_export.append(ftfd)
        # sometimes we don't get anything in fetched_content, so just ignore it
        except IndexError:
            pass
    return list_to_export


@measure
def process_fetched_feeds(
    config: configparser.ConfigParser, fetched_feeds: list, force: bool = False
) -> list:
    """Process previously fetched feeds"""
    feed_list = []
    for ftfd in fetched_feeds:
        # initialize feed object
        feed = Feed(
            input_content=ftfd,
            filters=config['filters'],
            formatting=config['formatting'],
        )
        # process feeds if there are updates since last run
        # or if the feed had never been processed
        # or if --force option is used
        if (
            feed.needs_update()
            or not path_exists(
                path=config['tenkan']['gemini_path'] + ftfd['title']
            )
            or force
        ):
            logging.info('Processing %s', ftfd['title'])
            feed.get_new_entries()
            feed_list.append(feed.export_content())
    return feed_list


@measure
def write_processed_feeds(
    args, config: configparser.ConfigParser, feed_list: list
) -> None:
    """Write files from processed feeds into gemini folder"""
    for files_data in feed_list:
        write_files(
            path=config['tenkan']['gemini_path'],
            data=files_data,
            max_num_entries=int(
                config['tenkan'].get('purge_feed_folder_after', '9999')
            ),
        )
        update_feed(
            file=args.feedsfile,
            feed_name=files_data['title'],
            hash_last_update=files_data['hash_last_update'],
        )
