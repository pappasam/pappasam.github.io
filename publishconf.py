"""Pelican production configuration file."""

# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-position
# isort: off

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = "https://samroeca.com"
RELATIVE_URLS = False
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
DELETE_OUTPUT_DIRECTORY = False
DISQUS_SITENAME = "pappasam-github-io"
GOOGLE_ANALYTICS = "G-FJ5WVT7YQL"
