#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Samuel Roeca'
SITENAME = 'Software Journeyman'

PATH = 'content'

TIMEZONE = 'EST'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# How to extract data from filename
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

# Ignore caching
LOAD_CONTENT_CACHE = False

#######################################################################
# Elegant theme-specific configurations
#######################################################################

THEME = 'pelican-themes/elegant'
STATIC_PATHS = ['theme/images', 'images']
SITEURL = 'http://localhost:8000'
USE_SHORTCUT_ICONS=True
JINJA_ENVIRONMENT = {
    'extensions': [
        'jinja2.ext.i18n',
    ],
}
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    'sitemap',
    'extract_toc',
    'tipue_search',  # this must be modified for now to work
    'neighbors',
]
DIRECT_TEMPLATES = ((
    'index',
    'tags',
    'categories',
    'archives',
    'search',
    '404',
))
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
