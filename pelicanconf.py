#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Samuel Roeca'
SITENAME = 'Software Journeyman'
SITEURL = 'http://localhost:8000'

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
SOCIAL = (
    ('github', 'https://github.com/pappasam'),
    ('linkedin-square', 'https://www.linkedin.com/in/samuel-roeca-23010735'),
    ('facebook','https://www.facebook.com/sam.roeca'),
    ('twitter', 'https://twitter.com/SamRoeca'),
    ('email', 'samuel.roeca@gmail.com'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# How to extract data from filename
# Currently, only does the slug
# FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
FILENAME_METADATA = '(?P<slug>.*)'

# Ignore caching
LOAD_CONTENT_CACHE = False

#######################################################################
# Elegant theme-specific configurations
#######################################################################

THEME = 'pelican-themes/elegant'
STATIC_PATHS = ['theme/images', 'images']
SOCIAL_PROFILE_LABEL = 'Contact Me'
USE_SHORTCUT_ICONS=True
JINJA_ENVIRONMENT = {
    'extensions': [
        'jinja2.ext.i18n',
    ],
}
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

#######################################################################
# Pelican Plugins
#######################################################################

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    'sitemap',
    'extract_toc',
    'tipue_search',        # this must be modified for now to work
    'neighbors',
    'assets',              # minifies css assets
    'filetime_from_git',
]

# tipue_search
#   see http://archerimagine.com/articles/pelican/integration-problem-with-elegant-theme.html#missing-icons-for-social-links
#   manually modify

# filetime_from_git
GIT_FILETIME_FROM_GIT = True
GIT_SHA_METADATA = True
GIT_GENERATE_PERMALINK = False
GIT_HISTORY_FOLLOWS_RENAME = True

# sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 1,
        'pages': 1,
        'indexes': 1,
    },
    'changefreqs': {
        'articles': 'always',
        'pages': 'always',
        'indexes': 'always',
    },
}
