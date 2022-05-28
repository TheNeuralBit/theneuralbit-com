#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Brian Hulette'
SITENAME = u'brian hulette'
SITESUBTITLE = u''
SITEURL = ''
STATIC_PATHS = ['images', 'media', 'code', 'keybase.txt']

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = False

from pelican_jupyter import markup as nb_markup
MARKUP = ('md', 'ipynb')

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["render_math", "pelican_gist", "liquid_tags.vimeo",
           "liquid_tags.soundcloud", "liquid_tags.speakerdeck",
           nb_markup, "simple_footnotes"]
MATH_JAX = {"color": "#000000"}
SOUNDCLOUD_CLIENT_ID = 'ebb0751100a870643e78012bc3394fe5'

# THEME CONFIGURATION
THEME = ".themes/theneuralbit"
HEADER_IMAGE = "/images/neuron_header.png"
MENUITEMS = (('blog', '/'),)
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False


GITHUB_USER = 'TheNeuralBit'
GITHUB_REPO_COUNT = 5
GITHUB_SKIP_FORK = True
TWITTER_USER = 'BrianHulette'

GRAVATAR_HASH = 'da1a82d2354ee7b8bcce6affa9227307'
GRAVATAR_WIDTH = 260

EXTRA_HEADER = \
"""<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script type="text/javascript" src="jquery.githubRepoWidget.min.js"></script>"""

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)
