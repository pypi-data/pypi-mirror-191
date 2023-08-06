# -*- coding: utf-8 -*-

""" files module : generated gemini feeds files management """

import logging
import pathlib
import shutil
from typing import Dict, Union

from feedgen.feed import FeedGenerator  # type: ignore


def path_exists(path: str) -> bool:
    """Check if feed path exists"""
    if pathlib.Path(path).is_dir():
        return True
    return False


def write_files(path: str, data: dict, max_num_entries: int) -> None:
    """
    Converts feed objects into files and write them in the feed folder
    """
    tpath = path
    path = path + data['title']
    pathlib.Path(path).mkdir(exist_ok=True)
    num_entries = 0
    # count entries in index file
    if pathlib.Path(f'{path}/index.gmi').is_file():
        num_entries = sum(1 for line in open(f'{path}/index.gmi'))  # pylint: disable=consider-using-with

    # if there is more articles than defined in max_num_entries, delete and rewrite
    if num_entries > max_num_entries:
        delete_folder(tpath, data['title'])

    index_file_write_header(path, data['title'])
    urls = []
    art_output = {}
    new_file = False
    for article in data['articles']:
        art_output = write_article(article, data, path)
        urls.append(art_output['url'])
        if art_output.get('new_file'):
            new_file = True
    index_file_write_footer(path)
    # no need to update atom file if no new articles (write_article func returns url list)
    if new_file:
        _rebuild_atom_file(path=path, data=data, urls=urls)


# def purge_folder(path: str) -> None:
#     """Purge folder with too many entries"""
#     logging.info('Purging %s folder', path)
#     files = [x for x in pathlib.Path(f'{path}').iterdir() if x.is_file()]
#     for file in files:
#         pathlib.Path.unlink(file)


def delete_folder(path: str, feed_name: str) -> None:
    """delete a feed folder"""
    if pathlib.Path(f'{path}{feed_name}/').exists():
        shutil.rmtree(f'{path}{feed_name}')
        logging.info('%s/%s folder deleted', path, feed_name)
    else:
        logging.info('folder %s%s not present, nothing to delete', path, feed_name)


def index_file_write_header(path: str, title: str) -> None:
    """Write index header"""
    with open(f'{path}/index.gmi', 'w') as index:
        index.write(f'# {title}\n\n')
        index.write('=> ../ ..\n')


def index_file_write_footer(path: str) -> None:
    """Write index footer"""
    with open(f'{path}/index.gmi', 'a') as index:
        index.write('\n=> atom.xml Atom feed\n')


def write_article(article: dict, data: dict, path: str) -> Dict[str, Union[bool, str]]:
    """Write individual article"""
    # prepare data for file format
    date = article['article_date']
    file_date = date.strftime('%Y-%m-%d_%H-%M-%S')
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    file_title = article['article_formatted_title']
    content = article['article_content']

    # we add the entry into index file
    with open(f'{path}/index.gmi', 'a') as index:
        index.write(f"=> {file_date}_{file_title}.gmi {date} - {article['article_title']}\n")

    new_file = False
    # write the file is it doesn't exist, obviously
    if not pathlib.Path(f'{path}/{file_date}_{file_title}.gmi').is_file():
        new_file = True
        logging.info('%s : adding entry %s', data['title'], file_title)
        # we write the entry file
        author = article['author'] if 'author' in article else None

        pathlib.Path(f'{path}/{file_date}_{file_title}.gmi').write_text(f"# {article['article_title']}\n\n=> {article['http_url']}\n\n{date}, {author}\n\n{content}")
    url = f"{data['gmi_url']}{data['title']}/{file_date}_{file_title}.gmi"
    return {'new_file': new_file, 'url': url}


def _rebuild_atom_file(path: str, data: dict, urls: list) -> None:
    """rebuilds the atom file into gmi folder"""

    atomfeed = FeedGenerator()
    atomfeed.id(data['gmi_url'])
    atomfeed.title(data['title'])
    atomfeed.updated = data['last_update']
    atomfeed.link(href=f"{data['gmi_url']}.atom.xml", rel='self')
    atomfeed.link(href=data['gmi_url'], rel='alternate')

    # rebuild all articles
    for art, article in enumerate(data['articles']):
        atomentry = atomfeed.add_entry()
        url = urls[art]
        atomentry.guid(url)
        atomentry.link(href=url, rel='alternate')
        atomentry.updated(article['updated'])
        atomentry.title(article['article_title'])

    atomfeed.atom_file(f'{path}/atom.xml', pretty=True)
    logging.info('Wrote Atom feed for %s', data['title'])
