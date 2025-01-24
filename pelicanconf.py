"""Pelican base configuration file."""

# core
#   https://docs.getpelican.com/en/stable/settings.html#basic-settings
#######################################################################
AUTHOR = "Samuel Roeca"
SITENAME = "Sam's world"
SITEURL = "http://localhost:8000"
PATH = "content"
TIMEZONE = "EST"
DEFAULT_LANG = "en"
FEED_ATOM = "feed/atom.xml"
FEED_RSS = "feed/rss.xml"
DEFAULT_PAGINATION = 10
FILENAME_METADATA = "(?P<slug>.*)"
LOAD_CONTENT_CACHE = False
TYPOGRIFY = True
EXTRA_PATH_METADATA = {
    "extra/custom.css": {
        "path": "static/custom.css",
    },
    "images/favicon.ico": {
        "path": "favicon.ico",
    },
    "images/sam-headshot-kepler-57x57.png": {
        "path": "apple-touch-icon-57x57.png",
    },
    "images/sam-headshot-kepler-72x72.png": {
        "path": "apple-touch-icon-72x72.png",
    },
    "images/sam-headshot-kepler-114x114.png": {
        "path": "apple-touch-icon-114x114.png",
    },
    "images/sam-headshot-kepler-144x144.png": {
        "path": "apple-touch-icon-144x144.png",
    },
    "images/sam-headshot-kepler-150x150.png": {
        "path": "apple-touch-icon.png",
    },
}


STATIC_PATHS = ["images", "gif", "extra"]
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

# theme: https://github.com/pappasam/pelican-alchemy
#######################################################################
THEME = "pelican-themes/pelican-theme/alchemy"
PYGMENTS_STYLE = "default"
SITESUBTITLE = "A stream of thought, whim, and wisdom"
DESCRIPTION = "Sam (Samuel) Roeca's personal blog about his thoughts/opinions."
SITEIMAGE = "/images/sam-headshot-kepler-200x200.jpg"
HIDE_AUTHORS = True
THEME_CSS_OVERRIDES = ["static/custom.css"]
ICONS = [
    ("fab fa-github", "https://github.com/pappasam"),
    ("fab fa-linkedin", "https://www.linkedin.com/in/samuel-roeca-23010735"),
    ("far fa-envelope", "mailto:samuel.roeca@gmail.com"),
    ("fas fa-code-branch", "https://github.com/pappasam/pappasam.github.io"),
    ("fas fa-rss-square", FEED_RSS),
    ("fas fa-rss", FEED_ATOM),
]
FOOTER_LINKS = [
    ("Categories", "categories.html"),
    ("Archives", "archives.html"),
    ("Tags", "tags.html"),
]

# plugins
#   https://github.com/pelican-plugins/sitemap#usage
#   https://github.com/pelican-plugins/neighbors#basic-usage
#   https://github.com/pelican-plugins/simple-footnotes#usage
#   https://github.com/johanvergeer/pelican-add-css-classes#usage
#######################################################################
PLUGINS = [
    "sitemap",
    "neighbors",
    "simple_footnotes",
    "add_css_classes",
]
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.5,
        "pages": 0.5,
        "indexes": 0.5,
    },
    "changefreqs": {
        "articles": "always",
        "pages": "always",
        "indexes": "always",
    },
}
ADD_CSS_CLASSES = {
    "table": ["table", "table-bordered", "table-striped"],
}
ADD_CSS_CLASSES_TO_PAGE = {}
ADD_CSS_CLASSES_TO_ARTICLE = {}
