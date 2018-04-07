#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Samuel Roeca'
SITENAME = 'Software Journeyman'

JINJA_ENVIRONMENT = {
    'extensions': [
        'jinja2.ext.i18n',
    ],
}

USE_FOLDER_AS_CATEGORY = True

PATH = 'content'

TIMEZONE = 'EST'

DEFAULT_LANG = 'en'
I18N_TEMPLATES_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# How to extract data from filename
# Currently, only does the slug
# FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
FILENAME_METADATA = '(?P<slug>.*)'

# Ignore caching
LOAD_CONTENT_CACHE = False

# static pathes for publishing
STATIC_PATHS = [
    'images',
    'theme/images'
]

#######################################################################
# Flex theme-specific configurations
#######################################################################

THEME = 'pelican-themes/Flex'

FAVICON = '/theme/images/favicon.ico'

SITESUBTITLE = "Sam Roeca's Blog"
SITEDESCRIPTION = "Samuel Roeca's blog"
SITEURL = 'http://localhost:8000'
SITELOGO = '/images/sam-headshot-kepler-300x300.jpg'

MAIN_MENU = True

LINKS = (
    # ('About', '/pages/about.html'),
)

SOCIAL = (
    ('github', 'https://github.com/pappasam'),
    ('linkedin-square', 'https://www.linkedin.com/in/samuel-roeca-23010735'),
    ('facebook','https://www.facebook.com/sam.roeca'),
    ('twitter', 'https://twitter.com/SamRoeca'),
    ('envelope-o', 'mailto:samuel.roeca@gmail.com'),
)

DIRECT_TEMPLATES = [
    'index',
    'categories',
    'authors',
    'archives',
    'tags',
]

MENUITEMS = (
    ('Archives', '/archives.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
)

#######################################################################
# Pelican Plugins
#######################################################################

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    'i18n_subsites',
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
