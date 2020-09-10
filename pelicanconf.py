"""Pelican base configuration file."""

# helpers
#######################################################################
_CUSTOM_CSS = "static/custom.css"

# core
#   https://docs.getpelican.com/en/stable/settings.html#basic-settings
#######################################################################
AUTHOR = "Samuel Roeca"
SITENAME = "Sam's Blog"
PATH = "content"
TIMEZONE = "EST"
DEFAULT_LANG = "en"
I18N_TEMPLATES_LANG = "en"
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DEFAULT_PAGINATION = 10
FILENAME_METADATA = "(?P<slug>.*)"
LOAD_CONTENT_CACHE = False
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

# theme: Flex
#   https://github.com/alexandrevicenzi/Flex/wiki/Custom-Settings
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
    ("linkedin", "https://www.linkedin.com/in/samuel-roeca-23010735"),
    ("facebook", "https://www.facebook.com/sam.roeca"),
    ("twitter", "https://twitter.com/SamRoeca"),
    (
        "youtube",
        "https://www.youtube.com/channel/UCjORdFKiDlqzzW7bWYqXuKA",
    ),
    ("envelope", "mailto:samuel.roeca@gmail.com"),
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
        "mdx_include": {"base_path": "./content/articles"},
    },
    "output_format": "html5",
}

# plugins
#   https://github.com/pelican-plugins/sitemap#usage
#   https://github.com/pelican-plugins/neighbors#basic-usage
#######################################################################
PLUGINS = [
    "sitemap",
    "neighbors",
]
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
