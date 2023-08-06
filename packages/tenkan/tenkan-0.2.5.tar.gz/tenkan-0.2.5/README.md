[![Build Status](https://drone.fqserv.eu/api/badges/takaoni/tenkan/status.svg)](https://drone.fqserv.eu/takaoni/tenkan)

# tenkan

Command line tool to convert HTTP RSS/Atom feeds to gemini format.

## Installation
```shell script
pip install tenkan
```

## Usage

Add a feed
```shell script
# Any valid RSS/Atom feed
tenkan add feedname url
```

Update content of feed list
```shell script
tenkan update
```

Delete feed
```shell script
tenkan delete feedname
```

List subscripted feeds
```shell script
tenkan list
```
## Options
A debug mode is avaible via --debug option.
If you want to use your configuration or feeds file in another place than default one, you can use --config and --feedsfile options.


## Configuration
tenkan searches for a configuration file at the following location:

`$XDG_CONFIG_HOME/tenkan/tenkan.conf`

### Example config
This can be found in tenkan.conf.example.

```ini
[tenkan]
gemini_path = /usr/local/gemini/
gemini_url = gemini://foo.bar/feeds/
# will purge feed folders having more than defined element count
# purge_feed_folder_after = 100

[filters]
# authors we don't want to read
# authors_blacklist = foo, bar
# blacklist of article titles, if provided, it won't be processed
# titles_blacklist = foo, bar
# blacklist of article links, if provided, it won't be processed
# links_blacklist = foo/bar.com, bar/foo, bla

[formatting]
# maximum article title size, 120 chars if not provided
# title_size = 120

# feeds with a truncated content
# will be fetched and converted using readability
# truncated_feeds = foo, bar
```

## Todolist
- [ ] Add a edit command
- [ ] Add a --feedname option to update command, to update a single feed
- [ ] Rewrite configuration checks
- [ ] add configuration option to log output into a logfile
- [ ] Improve tests
- [ ] Refactor needed parts like write_article
- [ ] (not sure if relevant) migrate images too, for gemini clients that can handle it

## Development
I recommend using pre-commit. The pre-commit configuration I use is located in .pre-commit-config.yamlfile.

Run pre-commit command before every pull request and fix the warnings or errors it produces.
