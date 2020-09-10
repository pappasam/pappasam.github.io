#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Samuel Roeca"
SITENAME = "Sam's Blog"

JINJA_ENVIRONMENT = {
    "extensions": [
        "jinja2.ext.i18n",
    ],
}

PATH = "content"

TIMEZONE = "EST"

DEFAULT_LANG = "en"
I18N_TEMPLATES_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# How to extract data from filename
# Currently, only does the slug
# FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
FILENAME_METADATA = "(?P<slug>.*)"

# Ignore caching
LOAD_CONTENT_CACHE = False

# static pathes for publishing
_CUSTOM_CSS = "static/custom.css"
EXTRA_PATH_METADATA = {
    "extra/custom.css": {
        "path": _CUSTOM_CSS,
    },
}
STATIC_PATHS = [
    "images",
    "theme/images",
    "gif",
    "extra",
]

# Code blocks
PYGMENTS_RST_OPTIONS = {
    # 'linenos': 'inline',  # enable line numbers
}

#######################################################################
# Flex theme-specific configurations
#######################################################################

THEME = "pelican-themes/Flex"

FAVICON = "/theme/images/favicon.ico"
PYGMENTS_STYLE = "tango"

SITESUBTITLE = "Sam's blog"
SITEDESCRIPTION = "Samuel Roeca's blog"
SITEURL = "http://localhost:8000"
SITELOGO = "/images/sam-headshot-kepler-300x300.jpg"

MAIN_MENU = True

CUSTOM_CSS = _CUSTOM_CSS

SOCIAL = (
    ("github", "https://github.com/pappasam"),
    ("linkedin-square", "https://www.linkedin.com/in/samuel-roeca-23010735"),
    ("facebook", "https://www.facebook.com/sam.roeca"),
    ("twitter", "https://twitter.com/SamRoeca"),
    (
        "youtube",
        "https://www.youtube.com/channel/UCjORdFKiDlqzzW7bWYqXuKA?view_as=subscriber",
    ),
    ("envelope-o", "mailto:samuel.roeca@gmail.com"),
)

DIRECT_TEMPLATES = [
    "index",
    "categories",
    "authors",
    "archives",
    "tags",
]

MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
        },
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {
            "permalink": True,
            "title": "Table of Contents",
            "marker": "[TOC]",
            "toc_depth": 3,
        },
        "mdx_include": {
            "base_path": "./content/articles"
        },
    },
    "output_format": "html5",
}

#######################################################################
# Pelican Plugins
#######################################################################

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = [
    "i18n_subsites",
    "sitemap",
    "neighbors",
    "assets",  # minifies css assets
]

# sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 1,
        "pages": 1,
        "indexes": 1,
    },
    "changefreqs": {
        "articles": "always",
        "pages": "always",
        "indexes": "always",
    },
}
