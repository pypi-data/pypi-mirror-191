# -*- coding: utf-8 -*-

""" feed module : feed object """

import logging
import re
import sys
from datetime import datetime, timezone
from typing import List

import requests  # type: ignore
from markdownify import markdownify  # type: ignore
from md2gemini import md2gemini  # type: ignore
from readability import Document  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from urllib3.util.retry import Retry

from tenkan.utils import measure


class Feed:
    """
    receives various feed data and applies necessary changes to make it usable into files
    """

    def __init__(
        self,
        input_content: dict,
        filters=None,
        formatting=None,
    ) -> None:
        self.content = input_content
        self.filters = filters
        self.formatting = formatting
        self.new_entries: list = []

    def needs_update(self) -> bool:
        """Checks if updates are available"""
        if not self.content['json_hash_last_update']:
            return True
        if (
            self.content['json_hash_last_update']
            != self.content['fetched_hash_last_update']
        ):
            return True
        return False

    @measure
    def get_new_entries(self) -> None:
        """Selects new entries depending on filters defined on config file"""
        for entry in self.content['fetched_content']['entries']:
            if (
                any(
                    x in entry['title']
                    for x in self.filters.get('titles_blacklist', '').split(
                        ','
                    )
                )
                or any(
                    x in entry['link']
                    for x in self.filters.get('links_blacklist', '').split(',')
                )
                or any(
                    # feedparser object can be problematic sometimes
                    # we need to check if we have an authors item
                    # AND we check if we can get it's name because it can be empty
                    # AND if we don't have any of these, we return a stupid string
                    # to match the str type which is expected
                    x
                    in (
                        entry.get('authors')
                        and entry.authors[0].get('name')
                        or 'random string'
                    )
                    for x in self.filters.get('authors_blacklist', '').split(
                        ','
                    )
                )
            ):
                self.content['fetched_content']['entries'].remove(entry)
                continue
            self.new_entries.append(entry)

    @measure
    def export_content(self) -> dict:
        """Exports properly formatted content"""
        # create feed item structure
        data_export: dict[str, List] = {
            'title': self.content['title'],
            'last_update': self.content['last_update'],
            'gmi_url': self.content['gmi_url'],
            'articles': [],
            'hash_last_update': self.content['fetched_hash_last_update'],
        }
        for article in self.new_entries:
            article_formatted_title = self._format_article_title(article)
            article_date = self._get_article_date(article)

            # 2 possibilities to get content : content['value'] or summary
            content = (
                article['content'][0]['value']
                if article.get('content')
                else article['summary']
            )

            article_content = self._format_article_content(
                content, link=article['link']
            )

            data_export['articles'].append(
                {
                    'article_title': article['title'],
                    'article_formatted_title': article_formatted_title,
                    'article_content': article_content,
                    'article_date': article_date,
                    'http_url': article['link'],
                    'updated': article_date,
                }
            )

        return data_export

    @classmethod
    def _get_article_date(cls, article: dict) -> datetime:
        """get date string and return datetime object"""
        try:
            return (
                datetime(
                    *article.get(
                        'published_parsed', article['updated_parsed']
                    )[:6]
                )
                .replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
            )
        except KeyError:
            logging.error(
                "Can't find a proper date field in article data, this should not happen !"
            )
            sys.exit(1)

    @measure
    def _format_article_title(self, article: dict) -> str:
        """title formatting to make it usable as a file title"""
        # truncate title size depending on title size
        maxlen = int(self.formatting.get('title_size', 120))
        if len(self.content['title']) + len(article['title']) > maxlen:
            maxlen = maxlen - len(self.content['title'])

        # We don't want multiline titles (yes, it happens)
        article['title'] = article['title'].replace('\n', '')[:maxlen]

        # remove special characters
        # probably not the best way to do it, as it seems there is performance issues here
        # to improve later if possible
        formatted_str = (
            article['title']
            .encode('utf8', 'ignore')
            .decode('utf8', 'ignore')
            .replace(' ', '-')
        )
        title = re.sub('[«»!@#$%^&*(){};:,./<>?/|`~=_+]', '', formatted_str)[
            :maxlen
        ]
        title = "".join(title.split())
        return title

    @measure
    def _format_article_content(self, content: str, link: str) -> str:
        """
        Formats article content from html to gmi
        Will use readability if the feed is truncated, so it should retrieve the full content
        """

        # conversion to readability format if asked
        if self.content['title'] in self.formatting.get(
            'truncated_feeds', 'アケオメ'
        ).split(','):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
            }

            req = requests.Session()
            retries = Retry(
                total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504],
            )
            req.mount('http://', HTTPAdapter(max_retries=retries))
            req.mount('https://', HTTPAdapter(max_retries=retries))
            res = req.get(url=link, headers=headers)

            content = Document(res.text).summary()

        # convert html -> md -> gemini
        article = md2gemini(markdownify(content))

        return article
